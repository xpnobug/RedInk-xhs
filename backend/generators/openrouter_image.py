"""OpenRouter 图片生成器"""
import logging
import time
import random
import base64
import requests
from typing import Dict, Any, Optional, List
from .base import ImageGeneratorBase
from ..utils.image_compressor import compress_image

logger = logging.getLogger(__name__)


def retry_on_error(max_retries: int = 3, base_delay: float = 2):
    """错误重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"请求失败，{delay:.1f}秒后重试 (尝试 {attempt + 2}/{max_retries}): {str(e)[:100]}")
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


class OpenRouterImageGenerator(ImageGeneratorBase):
    """OpenRouter 图片生成器
    
    支持通过 OpenRouter 平台调用 Gemini 2.5 Flash Image Preview 等图片生成模型。
    使用 Chat Completions API 格式，响应中包含生成的图片数据。
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        logger.debug("初始化 OpenRouterImageGenerator...")
        self.base_url = config.get('base_url', 'https://openrouter.ai/api')
        self.model = config.get('model', 'google/gemini-2.5-flash-image-preview')
        self.default_aspect_ratio = config.get('default_aspect_ratio', '1:1')
        self.max_tokens = config.get('max_tokens', 300)  # 降低默认值以减少成本
        self.default_temperature = config.get('temperature', 0.7)
        logger.info(f"OpenRouterImageGenerator 初始化完成: base_url={self.base_url}, model={self.model}, max_tokens={self.max_tokens}")

    def validate_config(self) -> bool:
        """验证配置是否有效"""
        if not self.api_key:
            logger.error("OpenRouter API Key 未配置")
            raise ValueError(
                "OpenRouter API Key 未配置。\n"
                "解决方案：在系统设置页面编辑该服务商，填写 API Key"
            )
        if not self.base_url:
            logger.error("OpenRouter Base URL 未配置")
            raise ValueError(
                "OpenRouter Base URL 未配置。\n"
                "解决方案：在系统设置页面编辑该服务商，填写 Base URL（如 https://openrouter.ai/api）"
            )
        return True

    def get_supported_aspect_ratios(self) -> List[str]:
        """获取支持的宽高比"""
        return ["1:1", "3:4", "4:3", "16:9", "9:16"]

    @retry_on_error(max_retries=3, base_delay=2)
    def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = None,
        temperature: float = None,
        model: str = None,
        reference_image: Optional[bytes] = None,
        reference_images: Optional[List[bytes]] = None,
        **kwargs
    ) -> bytes:
        """
        生成图片（使用 OpenRouter Chat Completions API）

        Args:
            prompt: 图片描述
            aspect_ratio: 宽高比（如 "1:1", "3:4", "16:9"）
            temperature: 创意度（0.0-1.0）
            model: 模型名称（如 google/gemini-2.5-flash-image-preview）
            reference_image: 单张参考图片数据（向后兼容）
            reference_images: 多张参考图片数据列表

        Returns:
            生成的图片二进制数据
        """
        self.validate_config()

        if aspect_ratio is None:
            aspect_ratio = self.default_aspect_ratio

        if temperature is None:
            temperature = self.default_temperature

        if model is None:
            model = self.model

        logger.info(f"OpenRouter 生成图片: model={model}, aspect_ratio={aspect_ratio}, temperature={temperature}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 构建消息内容
        message_content = []

        # 收集所有参考图片
        all_reference_images = []
        if reference_images and len(reference_images) > 0:
            all_reference_images.extend(reference_images)
        if reference_image and reference_image not in all_reference_images:
            all_reference_images.append(reference_image)

        # 如果有参考图片，添加到消息内容
        if all_reference_images:
            logger.debug(f"  添加 {len(all_reference_images)} 张参考图片")
            for idx, img_data in enumerate(all_reference_images):
                # 压缩图片到 200KB 以内
                compressed_img = compress_image(img_data, max_size_kb=200)
                logger.debug(f"  参考图 {idx}: {len(img_data)} -> {len(compressed_img)} bytes")
                base64_image = base64.b64encode(compressed_img).decode('utf-8')
                
                # OpenRouter 可能需要 data URI 格式或 URL 格式
                # 根据模型要求，这里使用 data URI
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                })

            # 增强提示词以利用参考图
            ref_count = len(all_reference_images)
            enhanced_prompt = f"""参考提供的 {ref_count} 张图片的风格（色彩、光影、构图、氛围），生成一张新图片。

新图片内容：{prompt}

要求：
1. 保持相似的色调和氛围
2. 使用相似的光影处理
3. 保持一致的画面质感
4. 如果参考图中有人物或产品，可以适当融入"""
            message_content.append({
                "type": "text",
                "text": enhanced_prompt
            })
        else:
            # 没有参考图，直接使用文本提示
            message_content.append({
                "type": "text",
                "text": prompt
            })

        # 构建请求体（OpenRouter Chat Completions 格式）
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message_content
                }
            ],
            "modalities": ["image", "text"],
            "max_tokens": self.max_tokens,
            "temperature": temperature,
            "image_config": {
                "aspect_ratio": aspect_ratio
            }
        }

        # 发送请求
        api_url = f"{self.base_url}/v1/chat/completions"
        logger.debug(f"  发送请求到: {api_url}")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=300
        )

        if response.status_code != 200:
            error_detail = response.text[:500]
            logger.error(f"OpenRouter 请求失败: status={response.status_code}, error={error_detail}")
            raise Exception(
                f"OpenRouter API 请求失败 (状态码: {response.status_code})\n"
                f"错误详情: {error_detail}\n"
                f"请求地址: {api_url}\n"
                "可能原因：\n"
                "1. API密钥无效或已过期\n"
                "2. 模型名称不正确\n"
                "3. 请求参数不符合API要求\n"
                "4. Base URL配置错误\n"
                "建议：检查API密钥、模型名称和base_url配置"
            )

        result = response.json()
        logger.debug(f"  API 响应: choices 长度={len(result.get('choices', []))}")

        # 提取图片数据（从 choices[0].message.images[0].image_url.url）
        try:
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                images = message.get("images", [])
                
                if images and len(images) > 0:
                    image_url_data = images[0].get("image_url", {})
                    data_uri = image_url_data.get("url", "")
                    
                    if data_uri:
                        # 解析 data URI (格式: data:image/png;base64,<base64_string>)
                        if data_uri.startswith('data:'):
                            # 提取 base64 部分
                            if ';base64,' in data_uri:
                                b64_string = data_uri.split(';base64,', 1)[1]
                            else:
                                # 尝试按逗号分割
                                b64_string = data_uri.split(',', 1)[1] if ',' in data_uri else data_uri
                        else:
                            # 如果不是 data URI，直接当作 base64
                            b64_string = data_uri

                        # 解码 base64
                        image_data = base64.b64decode(b64_string)
                        logger.info(f"✅ OpenRouter 图片生成成功: {len(image_data)} bytes")
                        return image_data
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"解析 OpenRouter 响应失败: {e}")
            logger.debug(f"完整响应: {str(result)[:1000]}")

        # 如果上面的解析失败，抛出错误
        logger.error(f"无法从响应中提取图片数据: {str(result)[:500]}")
        raise Exception(
            f"图片数据提取失败：未找到 choices[0].message.images[0].image_url.url 数据。\n"
            f"API响应片段: {str(result)[:500]}\n"
            "可能原因：\n"
            "1. API返回格式与预期不符\n"
            "2. 模型不支持图片生成\n"
            "3. 请求参数有误导致未生成图片\n"
            "建议：检查模型是否支持图片生成，查看完整错误日志"
        )
