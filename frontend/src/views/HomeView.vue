<template>
  <div class="container home-container">
    <!-- 图片网格轮播背景 -->
    <div class="showcase-background">
      <div class="showcase-grid" :style="{ transform: `translateY(-${scrollOffset}px)` }">
        <div v-for="(image, index) in showcaseImages" :key="index" class="showcase-item">
          <img :src="`/assets/showcase/${image}`" :alt="`封面 ${index + 1}`" />
        </div>
      </div>
      <div class="showcase-overlay"></div>
    </div>

    <!-- Hero Area -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="brand-pill">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
          AI 驱动的红墨创作助手
        </div>
        <div class="platform-slogan">
          让传播不再需要门槛，让创作从未如此简单
        </div>
        <h1 class="page-title">灵感一触即发</h1>
        <p class="page-subtitle">输入你的创意主题，让 AI 帮你生成爆款标题、正文和封面图</p>
      </div>

      <!-- Search Box (Composer Style) -->
      <div class="composer-container">
        <div class="composer-input-wrapper">
          <div class="search-icon-static">
             <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 21L16.65 16.65M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <textarea
            ref="textareaRef"
            v-model="topic"
            class="composer-textarea"
            placeholder="输入主题，例如：秋季显白美甲..."
            @keydown.enter.prevent="handleEnter"
            @input="adjustHeight"
            :disabled="loading"
            rows="1"
          ></textarea>
        </div>

        <!-- 已上传图片预览 -->
        <div v-if="uploadedImages.length > 0" class="uploaded-images-preview">
          <div
            v-for="(img, idx) in uploadedImages"
            :key="idx"
            class="uploaded-image-item"
          >
            <img :src="img.preview" :alt="`图片 ${idx + 1}`" />
            <button class="remove-image-btn" @click="removeImage(idx)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="upload-hint">
            这些图片将用于生成封面和内容参考
          </div>
        </div>

        <!-- Toolbar -->
        <div class="composer-toolbar">
          <div class="toolbar-left">
            <label class="tool-btn" :class="{ 'active': uploadedImages.length > 0 }" title="上传参考图">
              <input
                type="file"
                accept="image/*"
                multiple
                @change="handleImageUpload"
                :disabled="loading"
                style="display: none;"
              />
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
              <span v-if="uploadedImages.length > 0" class="badge-count">{{ uploadedImages.length }}</span>
            </label>
          </div>
          <div class="toolbar-right">
            <button
              class="btn btn-primary generate-btn"
              @click="handleGenerate"
              :disabled="!topic.trim() || loading"
            >
              <span v-if="loading" class="spinner-sm"></span>
              <span v-else>生成大纲</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Scenarios & Dashboard -->
    <div class="content-section">
    <!-- Dashboard Grid -->
    <div class="dashboard-grid">

      <!-- Recent Activity (Mockup) -->
      <div class="card feature-card">
        <div class="card-header">
          <div class="header-left">
             <div class="icon-box purple">
               <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
             </div>
             <h3 class="section-title-sm">最近创作</h3>
          </div>
          <button class="btn-text" @click="router.push('/history')">全部记录</button>
        </div>

        <div v-if="recentRecords.length > 0" class="recent-list">
          <div v-for="record in recentRecords" :key="record.id" class="recent-item" @click="loadRecord(record)">
            <div class="recent-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" color="#666"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            </div>
            <div class="recent-info">
              <div class="recent-title">{{ record.title }}</div>
              <div class="recent-date">{{ formatDate(record.updated_at) }}</div>
            </div>
            <div class="recent-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </div>
          </div>
        </div>
        <div v-else class="empty-state-mini">
          <p>暂无最近记录</p>
        </div>
      </div>

      <!-- Trending -->
      <div class="card feature-card">
        <div class="card-header">
          <div class="header-left">
             <div class="icon-box orange">
               <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
             </div>
             <h3 class="section-title-sm">全站热搜</h3>
          </div>
          <span class="refresh-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6"></path><path d="M1 20v-6h6"></path><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
          </span>
        </div>
        <div class="trend-list">
          <div class="trend-item">
            <span class="trend-rank rank-1">1</span>
            <span class="trend-name">#OOTD 每日穿搭</span>
            <span class="trend-hot">
               <svg width="12" height="12" viewBox="0 0 24 24" fill="#FF4D4F" stroke="#FF4D4F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.1.2-2.2.5-3.3a7 7 0 0 0 3 2.8Z"/></svg>
               234w
            </span>
          </div>
          <div class="trend-item">
            <span class="trend-rank rank-2">2</span>
            <span class="trend-name">#探店日记</span>
            <span class="trend-hot">
               <svg width="12" height="12" viewBox="0 0 24 24" fill="#FF6B81" stroke="#FF6B81" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.1.2-2.2.5-3.3a7 7 0 0 0 3 2.8Z"/></svg>
               189w
            </span>
          </div>
          <div class="trend-item">
            <span class="trend-rank rank-3">3</span>
            <span class="trend-name">#低脂减肥餐</span>
            <span class="trend-hot">
               <svg width="12" height="12" viewBox="0 0 24 24" fill="#FF9CA8" stroke="#FF9CA8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.1.2-2.2.5-3.3a7 7 0 0 0 3 2.8Z"/></svg>
               156w
            </span>
          </div>
          <div class="trend-item">
            <span class="trend-rank">4</span>
            <span class="trend-name">#家居改造</span>
            <span class="trend-hot">120w</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 首页页脚版权 -->
    <footer class="home-footer">
      <div class="footer-copyright">
        © 2025 <a href="https://github.com/HisMax/RedInk" target="_blank" rel="noopener noreferrer">RedInk</a> by 默子 (Histone)
      </div>
      <div class="footer-license-info">
        Licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener noreferrer">CC BY-NC-SA 4.0</a>
      </div>
    </footer>
    </div>

    <div v-if="error" class="error-toast">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGeneratorStore } from '../stores/generator'
import { generateOutline, getHistoryList, getHistory } from '../api'

const router = useRouter()
const store = useGeneratorStore()

const topic = ref('')
const loading = ref(false)
const error = ref('')
const recentRecords = ref<any[]>([])
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const isExpanded = ref(false)

// 图片网格轮播相关
const showcaseImages = ref<string[]>([])
const scrollOffset = ref(0)
let scrollInterval: ReturnType<typeof setInterval> | null = null

// 加载展示图片列表
const loadShowcaseImages = async () => {
  try {
    const response = await fetch('/assets/showcase_manifest.json')
    const data = await response.json()
    const originalImages = data.covers || []

    // 复制图片数组3次以实现无缝循环
    showcaseImages.value = [...originalImages, ...originalImages, ...originalImages]

    // 启动平滑滚动动画
    if (showcaseImages.value.length > 0) {
      scrollInterval = setInterval(() => {
        scrollOffset.value += 1

        // 计算网格总高度（每行约180px：164px图片 + 16px间距）
        const rowHeight = 180
        const itemsPerRow = 11
        const totalRows = Math.ceil(originalImages.length / itemsPerRow)
        const sectionHeight = totalRows * rowHeight

        // 滚动到第二组末尾时重置到第一组开始位置
        if (scrollOffset.value >= sectionHeight) {
          scrollOffset.value = 0
        }
      }, 30) // 每30ms移动1px，实现流畅滚动
    }
  } catch (e) {
    console.error('加载展示图片失败:', e)
  }
}

// 图片上传相关
interface UploadedImage {
  file: File
  preview: string
}
const uploadedImages = ref<UploadedImage[]>([])

const adjustHeight = () => {
  const el = textareaRef.value
  if (!el) return
  
  el.style.height = 'auto'
  const newHeight = Math.max(64, Math.min(el.scrollHeight, 200)) // Min 64px, Max 200px
  el.style.height = newHeight + 'px'
  
  isExpanded.value = newHeight > 64
}

const handleEnter = (e: KeyboardEvent) => {
  if (e.shiftKey) return // Allow multiline
  handleGenerate()
}

// 处理图片上传
const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files) return

  const files = Array.from(target.files)
  files.forEach((file) => {
    // 限制最多 5 张图片
    if (uploadedImages.value.length >= 5) {
      error.value = '最多只能上传 5 张图片'
      return
    }
    // 创建预览 URL
    const preview = URL.createObjectURL(file)
    uploadedImages.value.push({ file, preview })
  })

  // 清空 input，允许重复选择同一文件
  target.value = ''
}

// 移除图片
const removeImage = (index: number) => {
  const img = uploadedImages.value[index]
  // 释放预览 URL
  URL.revokeObjectURL(img.preview)
  uploadedImages.value.splice(index, 1)
}

const loadRecent = async () => {
  try {
    const res = await getHistoryList(1, 4)
    if (res.success) {
      recentRecords.value = res.records
    }
  } catch (e) {
    // ignore
  }
}

const formatDate = (str: string) => {
  const d = new Date(str)
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${d.getMinutes().toString().padStart(2, '0')}`
}

const loadRecord = async (record: any) => {
   // Simple load for edit
   try {
     const res = await getHistory(record.id)
     if (res.success && res.record) {
        store.setTopic(res.record.title)
        store.setOutline(res.record.outline.raw, res.record.outline.pages)
        store.recordId = res.record.id
        router.push('/outline')
     }
   } catch(e) {
     console.error(e)
   }
}

const handleGenerate = async () => {
  if (!topic.value.trim()) return

  loading.value = true
  error.value = ''

  try {
    // 获取上传的图片文件列表
    const imageFiles = uploadedImages.value.map(img => img.file)

    const result = await generateOutline(
      topic.value.trim(),
      imageFiles.length > 0 ? imageFiles : undefined
    )

    if (result.success && result.pages) {
      store.setTopic(topic.value.trim())
      store.setOutline(result.outline || '', result.pages)
      store.recordId = null  // 重置历史记录ID,确保创建新记录

      // 如果有上传图片，保存到 store 中用于图片生成
      if (imageFiles.length > 0) {
        store.userImages = imageFiles
      } else {
        store.userImages = []
      }

      // 清理预览 URL
      uploadedImages.value.forEach(img => URL.revokeObjectURL(img.preview))
      uploadedImages.value = []

      router.push('/outline')
    } else {
      error.value = result.error || '生成大纲失败'
    }
  } catch (err: any) {
    error.value = err.message || '网络错误，请重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRecent()
  loadShowcaseImages()
})

onUnmounted(() => {
  if (scrollInterval) {
    clearInterval(scrollInterval)
  }
})
</script>

<style scoped>
/* 图片网格轮播背景 */
.showcase-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: -1;
  overflow: hidden;
}

.showcase-grid {
  display: grid;
  grid-template-columns: repeat(11, 1fr);
  gap: 16px;
  padding: 20px;
  width: 100%;
  will-change: transform;
  opacity: 0.8; /* 稍微降低不透明度，减少干扰 */
}

.showcase-item {
  width: 100%;
  aspect-ratio: 3 / 4;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: transform 0.3s ease;
}

.showcase-item:hover {
  transform: scale(1.02);
}

.showcase-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.showcase-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(247, 248, 250, 0.85) 0%,
    rgba(247, 248, 250, 0.8) 30%,
    rgba(247, 248, 250, 0.7) 100%
  );
  backdrop-filter: blur(4px);
}

.home-container {
  max-width: 1000px; /* 稍微收窄，增加聚焦感 */
  padding-top: 40px;
  position: relative;
  z-index: 1;
}

/* Section Headers */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 4px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.link-more {
  font-size: 13px;
  color: var(--text-sub);
  cursor: pointer;
  transition: color 0.2s;
  font-weight: 500;
}
.link-more:hover { color: var(--primary); }

/* Hero Section */
.hero-section {
  text-align: center;
  margin-bottom: 48px;
  padding: 60px 40px;
  animation: fadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
  background: var(--bg-glass-heavy);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  backdrop-filter: var(--backdrop-blur);
  border: 1px solid rgba(255, 255, 255, 0.6);
}

/* Content Section */
.content-section {
  background: var(--bg-glass-heavy);
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: var(--shadow-lg);
  backdrop-filter: var(--backdrop-blur);
  border: 1px solid rgba(255, 255, 255, 0.6);
  margin-top: 32px;
}

.hero-content {
  margin-bottom: 48px;
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

.brand-pill {
  display: inline-flex;
  align-items: center;
  padding: 6px 16px;
  background: rgba(255, 36, 66, 0.06);
  color: var(--primary);
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
  letter-spacing: 0.5px;
  border: 1px solid rgba(255, 36, 66, 0.1);
  transition: all 0.3s ease;
}

.brand-pill:hover {
  background: rgba(255, 36, 66, 0.1);
  transform: translateY(-1px);
}

.platform-slogan {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 16px;
  line-height: 1.4;
  letter-spacing: -0.02em;
}

.page-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #FF2442 0%, #FF6B81 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 18px;
  color: var(--text-sub);
  margin-top: 16px;
  line-height: 1.6;
  font-weight: 400;
}

/* Composer Container */
.composer-container {
  max-width: 720px;
  margin: 0 auto;
  position: relative;
  background: #FFFFFF;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  padding: 8px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.composer-container:focus-within {
  box-shadow: var(--shadow-xl), 0 0 0 2px var(--primary-fade);
  border-color: var(--primary);
  transform: translateY(-2px);
}

.composer-input-wrapper {
  position: relative;
  display: flex;
  align-items: flex-start;
  padding: 12px 16px;
}

.search-icon-static {
  margin-top: 10px;
  margin-right: 12px;
  color: var(--text-placeholder);
}

.composer-textarea {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-main);
  resize: none;
  padding: 10px 0;
  min-height: 48px;
  font-family: inherit;
}

.composer-textarea:focus {
  outline: none;
}

.composer-textarea::placeholder {
  color: var(--text-placeholder);
}

/* Toolbar */
.composer-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px 12px;
  border-top: 1px solid var(--border-color);
  margin-top: 8px;
}

.tool-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  color: var(--text-sub);
  transition: all 0.2s;
  position: relative;
}

.tool-btn:hover {
  background: #F3F4F6;
  color: var(--primary);
}

.tool-btn.active {
  color: var(--primary);
  background: var(--primary-fade);
}

.badge-count {
  position: absolute;
  top: -2px;
  right: -2px;
  background: var(--primary);
  color: white;
  font-size: 10px;
  font-weight: 700;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  border: 2px solid #fff;
}

.generate-btn {
  border-radius: 100px;
  padding: 10px 24px;
  font-size: 15px;
  font-weight: 600;
  background: var(--primary);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(255, 36, 66, 0.25);
}

.generate-btn:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(255, 36, 66, 0.35);
}

.generate-btn:disabled {
  background: var(--text-placeholder);
  cursor: not-allowed;
  box-shadow: none;
}

/* Uploaded Images */
.uploaded-images-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 12px 16px;
  background: #F9FAFB;
  border-radius: var(--radius-md);
  margin: 0 12px 12px;
}

.uploaded-image-item {
  position: relative;
  width: 64px;
  height: 64px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(0,0,0,0.05);
}

.uploaded-image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: all 0.2s;
  backdrop-filter: blur(4px);
}

.uploaded-image-item:hover .remove-image-btn {
  opacity: 1;
}

.remove-image-btn:hover {
  background: var(--primary);
  transform: scale(1.1);
}

.upload-hint {
  flex: 1;
  font-size: 12px;
  color: var(--text-secondary);
  text-align: right;
  font-style: italic;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
  animation: slideUp 0.6s ease-out 0.2s backwards;
}

.feature-card {
  height: 100%;
  min-height: 320px;
  display: flex;
  flex-direction: column;
  padding: 0; /* padding moved to inner elements */
  background: transparent;
  box-shadow: none;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 0 4px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-title-sm {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: var(--text-main);
}

.icon-box {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.icon-box.purple {
  background: linear-gradient(135deg, #9F7AEA 0%, #805AD5 100%);
  box-shadow: 0 8px 16px rgba(128, 90, 213, 0.25);
}

.icon-box.orange {
  background: linear-gradient(135deg, #F6AD55 0%, #ED8936 100%);
  box-shadow: 0 8px 16px rgba(237, 137, 54, 0.25);
}

.btn-text {
  background: none;
  border: none;
  color: var(--text-sub);
  font-size: 14px;
  cursor: pointer;
  font-weight: 500;
  transition: color 0.2s;
}
.btn-text:hover { color: var(--primary); }

/* Recent List */
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: var(--radius-md);
  background: #FFFFFF;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  box-shadow: var(--shadow-sm);
}

.recent-item:hover {
  background: #FFFFFF;
  border-color: var(--primary-fade);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.recent-icon {
  width: 40px;
  height: 40px;
  background: #F3F4F6;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-sub);
  transition: all 0.2s;
}

.recent-item:hover .recent-icon {
  background: var(--primary-light);
  color: var(--primary);
}

.recent-info {
  flex: 1;
  overflow: hidden;
}

.recent-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.recent-date {
  font-size: 12px;
  color: var(--text-secondary);
}

.recent-arrow {
  color: var(--text-placeholder);
  transition: all 0.2s;
}

.recent-item:hover .recent-arrow {
  color: var(--primary);
  transform: translateX(4px);
}

.empty-state-mini {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 14px;
  background: #F9FAFB;
  border-radius: var(--radius-md);
  border: 1px dashed var(--border-color);
  text-align: center;
  padding: 40px;
}

/* Trend List */
.trend-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.trend-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #FFFFFF;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: all 0.2s;
}

.trend-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.trend-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-secondary);
  margin-right: 12px;
  font-family: 'Monaco', monospace;
}

.trend-rank.rank-1 { color: #FFD700; }
.trend-rank.rank-2 { color: #C0C0C0; }
.trend-rank.rank-3 { color: #CD7F32; }

.trend-name {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main);
}

.trend-hot {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: var(--text-sub);
  font-weight: 500;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

.error-toast {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  background: #FEF2F2;
  color: #DC2626;
  padding: 12px 24px;
  border-radius: 100px;
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid #FEE2E2;
  z-index: 1000;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Responsive */
@media (max-width: 768px) {
  .showcase-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    padding: 12px;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .scenarios-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 首页页脚样式 */
.home-footer {
  margin-top: 48px;
  padding: 32px 0 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  text-align: center;
}

.footer-copyright {
  font-size: 14px;
  color: #666;
  font-weight: 500;
  margin-bottom: 8px;
}

.footer-copyright a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.footer-copyright a:hover {
  color: var(--primary-hover);
  text-decoration: underline;
}

.footer-license-info {
  font-size: 13px;
  color: #999;
}

.footer-license-info a {
  color: #777;
  text-decoration: none;
  transition: all 0.2s ease;
}

.footer-license-info a:hover {
  color: var(--primary);
  text-decoration: underline;
}
</style>
