<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">系统设置</h1>
      <p class="page-subtitle">配置文本生成和图片生成的 API 服务</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载配置中...</p>
    </div>

    <div v-else class="settings-container">
      <!-- Tabs Navigation -->
      <div class="tabs-nav">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'text' }"
          @click="activeTab = 'text'"
        >
          文本生成
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'image' }"
          @click="activeTab = 'image'"
        >
          图片生成
        </button>
      </div>

      <!-- 文本生成配置 -->
      <div v-if="activeTab === 'text'" class="card tab-content">
        <div class="section-header">
          <div>
            <h2 class="section-title">文本生成配置</h2>
            <p class="section-desc">用于生成小红书图文大纲</p>
          </div>
          <button class="btn btn-small" @click="openAddTextProviderModal">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            添加
          </button>
        </div>

        <!-- 服务商列表 -->
        <div class="provider-list">
          <div
            v-for="(provider, name) in textConfig.providers"
            :key="name"
            class="provider-item"
            :class="{ active: textConfig.active_provider === name }"
          >
            <div class="provider-info">
              <div class="provider-header">
                <div class="provider-title">
                  <span class="provider-name">{{ name }}</span>
                  <span class="provider-type">{{ getTypeLabel(provider.type) }}</span>
                </div>
                <div class="provider-meta">
                  <div class="meta-item" title="模型">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                    <span class="meta-text" :title="provider.model">{{ provider.model }}</span>
                  </div>
                  <div class="meta-item" title="API Key">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"></path></svg>
                    <span class="meta-text code">{{ provider.api_key_masked || '未配置' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="provider-actions">
              <div class="status-section">
                <span v-if="textConfig.active_provider === name" class="status-text active">
                  <span class="status-dot"></span>
                  使用中
                </span>
                <button
                  v-else
                  class="btn-activate"
                  @click="activateTextProvider(name as string)"
                >
                  激活
                </button>
              </div>
              
              <div class="action-divider"></div>

              <div class="icon-actions">
                <button class="btn-icon" @click="testTextProviderInList(name as string, provider)" title="测试连接">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                  </svg>
                </button>
                <button class="btn-icon" @click="openEditTextProviderModal(name as string, provider)" title="编辑">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button
                  class="btn-icon danger"
                  @click="deleteTextProvider(name as string)"
                  v-if="Object.keys(textConfig.providers).length > 1"
                  title="删除"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 图片生成配置 -->
      <div v-if="activeTab === 'image'" class="card tab-content">
        <div class="section-header">
          <div>
            <h2 class="section-title">图片生成配置</h2>
            <p class="section-desc">用于生成小红书配图</p>
          </div>
          <button class="btn btn-small" @click="openAddImageProviderModal">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            添加
          </button>
        </div>

        <!-- 服务商列表 -->
        <div class="provider-list">
          <div
            v-for="(provider, name) in imageConfig.providers"
            :key="name"
            class="provider-item"
            :class="{ active: imageConfig.active_provider === name }"
          >
            <div class="provider-info">
              <div class="provider-header">
                <div class="provider-title">
                  <span class="provider-name">{{ name }}</span>
                  <span class="provider-type">{{ getTypeLabel(provider.type) }}</span>
                </div>
                <div class="provider-meta">
                  <div class="meta-item" title="模型">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                    <span class="meta-text" :title="provider.model">{{ provider.model }}</span>
                  </div>
                  <div class="meta-item" title="API Key">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"></path></svg>
                    <span class="meta-text code">{{ provider.api_key_masked || '未配置' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="provider-actions">
              <div class="status-section">
                <span v-if="imageConfig.active_provider === name" class="status-text active">
                  <span class="status-dot"></span>
                  使用中
                </span>
                <button
                  v-else
                  class="btn-activate"
                  @click="activateImageProvider(name as string)"
                >
                  激活
                </button>
              </div>
              
              <div class="action-divider"></div>

              <div class="icon-actions">
                <button class="btn-icon" @click="testImageProviderInList(name as string, provider)" title="测试连接">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                  </svg>
                </button>
                <button class="btn-icon" @click="openEditImageProviderModal(name as string, provider)" title="编辑">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button
                  class="btn-icon danger"
                  @click="deleteImageProvider(name as string)"
                  v-if="Object.keys(imageConfig.providers).length > 1"
                  title="删除"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑/添加文本生成服务商弹窗 -->
    <div v-if="showTextProviderModal" class="modal-overlay" @click="closeTextProviderModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingTextProvider ? '编辑服务商' : '添加服务商' }}</h3>
          <button class="close-btn" @click="closeTextProviderModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group" v-if="!editingTextProvider">
            <label>服务商名称</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                <line x1="7" y1="7" x2="7.01" y2="7"></line>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="textProviderForm.name"
                placeholder="例如: openai"
              />
            </div>
            <span class="form-hint">唯一标识，用于区分不同服务商</span>
          </div>
          <div class="form-group">
            <label>类型</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
              <select class="form-select" v-model="textProviderForm.type">
                <option value="google_gemini">Google Gemini</option>
                <option value="openai_compatible">OpenAI 兼容接口</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>API Key</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"></path>
              </svg>
              <input
                type="password"
                class="form-input"
                v-model="textProviderForm.api_key"
                :placeholder="editingTextProvider ? '留空则保持原有 Key 不变' : '输入 API Key'"
              />
            </div>
            <span class="form-hint" v-if="editingTextProvider && hasExistingApiKey(textProviderForm)">已配置 API Key，留空表示不修改</span>
          </div>
          <div class="form-group" v-if="textProviderForm.type === 'openai_compatible'">
            <label>Base URL</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="textProviderForm.base_url"
                placeholder="例如: https://api.openai.com"
              />
            </div>
          </div>
          <div class="form-group">
            <label>模型</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="textProviderForm.model"
                placeholder="例如: gpt-4o"
              />
            </div>
          </div>
          <div class="form-group" v-if="textProviderForm.type === 'openai_compatible'">
            <label>API 端点路径</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="textProviderForm.endpoint_type"
                placeholder="例如: /v1/chat/completions"
              />
            </div>
            <span class="form-hint">
              默认端点：/v1/chat/completions（大多数 OpenAI 兼容 API 使用此端点）
            </span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn" @click="closeTextProviderModal">取消</button>
          <button
            class="btn btn-secondary"
            @click="testTextConnection"
            :disabled="testingText || (!textProviderForm.api_key && !editingTextProvider)"
          >
            <span v-if="testingText" class="spinner-small"></span>
            {{ testingText ? '测试中...' : '测试连接' }}
          </button>
          <button class="btn btn-primary" @click="saveTextProvider">
            {{ editingTextProvider ? '保存' : '添加' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑/添加图片生成服务商弹窗 -->
    <div v-if="showImageProviderModal" class="modal-overlay" @click="closeImageProviderModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingImageProvider ? '编辑服务商' : '添加服务商' }}</h3>
          <button class="close-btn" @click="closeImageProviderModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group" v-if="!editingImageProvider">
            <label>服务商名称</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                <line x1="7" y1="7" x2="7.01" y2="7"></line>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="imageProviderForm.name"
                placeholder="例如: google_genai"
              />
            </div>
            <span class="form-hint">唯一标识，用于区分不同服务商</span>
          </div>
          <div class="form-group">
            <label>类型</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
              <select class="form-select" v-model="imageProviderForm.type">
                <option value="google_genai">Google GenAI</option>
                <option value="image_api">OpenAI 兼容接口</option>
                <option value="openrouter">OpenRouter</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>API Key</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"></path>
              </svg>
              <input
                type="password"
                class="form-input"
                v-model="imageProviderForm.api_key"
                :placeholder="editingImageProvider ? '留空则保持原有 Key 不变' : '输入 API Key'"
              />
            </div>
            <span class="form-hint" v-if="editingImageProvider && hasExistingApiKey(imageProviderForm)">已配置 API Key，留空表示不修改</span>
          </div>
          <div class="form-group" v-if="imageProviderForm.type === 'image_api' || imageProviderForm.type === 'openrouter'">
            <label>Base URL</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="imageProviderForm.base_url"
                :placeholder="imageProviderForm.type === 'openrouter' ? '例如: https://openrouter.ai/api' : '例如: https://api.openai.com'"
              />
            </div>
          </div>
          <div class="form-group">
            <label>模型</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="imageProviderForm.model"
                placeholder="例如: gemini-3-pro-image-preview"
              />
            </div>
          </div>
          <div class="form-group" v-if="imageProviderForm.type === 'image_api'">
            <label>API 端点路径</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
              <input
                type="text"
                class="form-input"
                v-model="imageProviderForm.endpoint_type"
                placeholder="例如: /v1/images/generations 或 /v1/chat/completions"
              />
            </div>
            <span class="form-hint">
              常用端点：/v1/images/generations（标准图片生成）、/v1/chat/completions（即梦等返回链接的 API）
            </span>
          </div>
          <div class="form-group">
            <label class="toggle-label">
              <span>高并发模式</span>
              <div class="toggle-switch" :class="{ active: imageProviderForm.high_concurrency }" @click="imageProviderForm.high_concurrency = !imageProviderForm.high_concurrency">
                <div class="toggle-slider"></div>
              </div>
            </label>
            <span class="form-hint">启用后将并行生成图片，速度更快但对 API 质量要求较高。GCP 300$ 试用账号不建议启用。</span>
          </div>
          <div class="form-group">
            <label class="toggle-label">
              <span>短 Prompt 模式</span>
              <div class="toggle-switch" :class="{ active: imageProviderForm.short_prompt }" @click="imageProviderForm.short_prompt = !imageProviderForm.short_prompt">
                <div class="toggle-slider"></div>
              </div>
            </label>
            <span class="form-hint">启用后使用精简版提示词，适合有字符限制的 API（如即梦 1600 字符限制）。</span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn" @click="closeImageProviderModal">取消</button>
          <button
            class="btn btn-secondary"
            @click="testImageConnection"
            :disabled="testingImage || (!imageProviderForm.api_key && !editingImageProvider)"
          >
            <span v-if="testingImage" class="spinner-small"></span>
            {{ testingImage ? '测试中...' : '测试连接' }}
          </button>
          <button class="btn btn-primary" @click="saveImageProvider">
            {{ editingImageProvider ? '保存' : '添加' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getConfig, updateConfig, testConnection, type Config } from '../api'

const loading = ref(true)
const saving = ref(false)
const testingText = ref(false)
const testingImage = ref(false)
const activeTab = ref<'text' | 'image'>('text')

// 文本生成配置
const textConfig = ref<{
  active_provider: string
  providers: Record<string, any>
}>({
  active_provider: '',
  providers: {}
})

// 图片生成配置
const imageConfig = ref<{
  active_provider: string
  providers: Record<string, any>
}>({
  active_provider: '',
  providers: {}
})

// 文本服务商弹窗
const showTextProviderModal = ref(false)
const editingTextProvider = ref<string | null>(null)
const textProviderForm = ref({
  name: '',
  type: 'openai_compatible',
  api_key: '',
  base_url: '',
  model: '',
  endpoint_type: '/v1/chat/completions',
  _has_api_key: false // 标记是否已有 API Key
})

// 图片服务商弹窗
const showImageProviderModal = ref(false)
const editingImageProvider = ref<string | null>(null)
const imageProviderForm = ref({
  name: '',
  type: '',
  api_key: '',
  base_url: '',
  model: '',
  high_concurrency: false,
  short_prompt: false,
  endpoint_type: '/v1/images/generations',
  _has_api_key: false
})

// 类型标签映射
function getTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'google_gemini': 'Gemini',
    'openai_compatible': 'OpenAI',
    'google_genai': 'Google GenAI'
  }
  return labels[type] || type
}

// 检查是否已有 API Key
function hasExistingApiKey(form: any): boolean {
  return form._has_api_key === true
}

// 加载配置
async function loadConfig() {
  loading.value = true
  try {
    const result = await getConfig()
    if (result.success && result.config) {
      textConfig.value = {
        active_provider: result.config.text_generation.active_provider,
        providers: result.config.text_generation.providers
      }
      imageConfig.value = result.config.image_generation
    } else {
      alert('加载配置失败: ' + (result.error || '未知错误'))
    }
  } catch (e) {
    alert('加载配置失败: ' + String(e))
  } finally {
    loading.value = false
  }
}

// 保存配置
async function saveConfig() {
  saving.value = true
  try {
    const config: Partial<Config> = {
      text_generation: {
        active_provider: textConfig.value.active_provider,
        providers: textConfig.value.providers
      },
      image_generation: imageConfig.value
    }

    const result = await updateConfig(config)
    if (result.success) {
      alert(result.message || '配置已保存')
    } else {
      alert('保存失败: ' + (result.error || '未知错误'))
    }
  } catch (e) {
    alert('保存失败: ' + String(e))
  } finally {
    saving.value = false
  }
}

// 激活文本服务商
async function activateTextProvider(name: string) {
  textConfig.value.active_provider = name
  await autoSaveConfig()
}

// 激活图片服务商
async function activateImageProvider(name: string) {
  imageConfig.value.active_provider = name
  await autoSaveConfig()
}

// 自动保存配置
async function autoSaveConfig() {
  try {
    const config: Partial<Config> = {
      text_generation: {
        active_provider: textConfig.value.active_provider,
        providers: textConfig.value.providers
      },
      image_generation: imageConfig.value
    }

    const result = await updateConfig(config)
    if (result.success) {
      // 重新加载配置以获取最新的脱敏 API Key
      await loadConfig()
    }
  } catch (e) {
    console.error('自动保存失败:', e)
  }
}

// 打开添加文本服务商弹窗
function openAddTextProviderModal() {
  editingTextProvider.value = null
  textProviderForm.value = {
    name: '',
    type: 'openai_compatible',
    api_key: '',
    base_url: '',
    model: '',
    endpoint_type: '/v1/chat/completions',
    _has_api_key: false
  }
  showTextProviderModal.value = true
}

// 打开编辑文本服务商弹窗
function openEditTextProviderModal(name: string, provider: any) {
  editingTextProvider.value = name
  textProviderForm.value = {
    name: name,
    type: provider.type || 'openai_compatible',
    api_key: '', // 不显示已有的 key，让用户重新输入才会更新
    base_url: provider.base_url || '',
    model: provider.model || '',
    endpoint_type: provider.endpoint_type || '/v1/chat/completions',
    _has_api_key: !!provider.api_key // 标记是否已有 key
  }
  showTextProviderModal.value = true
}

// 关闭文本服务商弹窗
function closeTextProviderModal() {
  showTextProviderModal.value = false
  editingTextProvider.value = null
}

// 保存文本服务商
async function saveTextProvider() {
  const name = editingTextProvider.value || textProviderForm.value.name

  if (!name) {
    alert('请填写服务商名称')
    return
  }

  if (!textProviderForm.value.type) {
    alert('请选择服务商类型')
    return
  }

  // 新增时必须填写 API Key
  if (!editingTextProvider.value && !textProviderForm.value.api_key) {
    alert('请填写 API Key')
    return
  }

  const existingProvider = textConfig.value.providers[name] || {}

  const providerData: any = {
    type: textProviderForm.value.type,
    model: textProviderForm.value.model
  }

  // 如果填写了新的 API Key，使用新的；否则保留原有的
  if (textProviderForm.value.api_key) {
    providerData.api_key = textProviderForm.value.api_key
  } else if (existingProvider.api_key) {
    providerData.api_key = existingProvider.api_key
  }

  if (textProviderForm.value.base_url) {
    providerData.base_url = textProviderForm.value.base_url
  }

  // 如果是 OpenAI 兼容接口，保存 endpoint_type
  if (textProviderForm.value.type === 'openai_compatible') {
    providerData.endpoint_type = textProviderForm.value.endpoint_type
  }

  textConfig.value.providers[name] = providerData

  closeTextProviderModal()
  await autoSaveConfig()
}

// 删除文本服务商
async function deleteTextProvider(name: string) {
  if (confirm(`确定要删除服务商 "${name}" 吗？`)) {
    delete textConfig.value.providers[name]
    if (textConfig.value.active_provider === name) {
      textConfig.value.active_provider = ''
    }
    await autoSaveConfig()
  }
}

// 打开添加图片服务商弹窗
function openAddImageProviderModal() {
  editingImageProvider.value = null
  imageProviderForm.value = {
    name: '',
    type: 'image_api',
    api_key: '',
    base_url: '',
    model: '',
    high_concurrency: false,
    short_prompt: false,
    endpoint_type: '/v1/images/generations',
    _has_api_key: false
  }
  showImageProviderModal.value = true
}

// 打开编辑图片服务商弹窗
function openEditImageProviderModal(name: string, provider: any) {
  editingImageProvider.value = name
  imageProviderForm.value = {
    name: name,
    type: provider.type || '',
    api_key: '',
    base_url: provider.base_url || '',
    model: provider.model || '',
    high_concurrency: provider.high_concurrency || false,
    short_prompt: provider.short_prompt || false,
    endpoint_type: provider.endpoint_type || '/v1/images/generations',
    _has_api_key: !!provider.api_key
  }
  showImageProviderModal.value = true
}

// 关闭图片服务商弹窗
function closeImageProviderModal() {
  showImageProviderModal.value = false
  editingImageProvider.value = null
}

// 保存图片服务商
async function saveImageProvider() {
  const name = editingImageProvider.value || imageProviderForm.value.name

  if (!name) {
    alert('请填写服务商名称')
    return
  }

  if (!imageProviderForm.value.type) {
    alert('请填写服务商类型')
    return
  }

  // 新增时必须填写 API Key
  if (!editingImageProvider.value && !imageProviderForm.value.api_key) {
    alert('请填写 API Key')
    return
  }

  const existingProvider = imageConfig.value.providers[name] || {}

  const providerData: any = {
    type: imageProviderForm.value.type,
    model: imageProviderForm.value.model,
    high_concurrency: imageProviderForm.value.high_concurrency,
    short_prompt: imageProviderForm.value.short_prompt
  }

  // 如果是 OpenAI 兼容接口，保存 endpoint_type
  if (imageProviderForm.value.type === 'image_api') {
    providerData.endpoint_type = imageProviderForm.value.endpoint_type
  }

  // 如果填写了新的 API Key，使用新的；否则保留原有的
  if (imageProviderForm.value.api_key) {
    providerData.api_key = imageProviderForm.value.api_key
  } else if (existingProvider.api_key) {
    providerData.api_key = existingProvider.api_key
  }

  if (imageProviderForm.value.base_url) {
    providerData.base_url = imageProviderForm.value.base_url
  }

  imageConfig.value.providers[name] = providerData

  closeImageProviderModal()
  await autoSaveConfig()
}

// 删除图片服务商
async function deleteImageProvider(name: string) {
  if (confirm(`确定要删除服务商 "${name}" 吗？`)) {
    delete imageConfig.value.providers[name]
    if (imageConfig.value.active_provider === name) {
      imageConfig.value.active_provider = ''
    }
    await autoSaveConfig()
  }
}

// 测试文本服务商连接
async function testTextConnection() {
  testingText.value = true
  try {
    const result = await testConnection({
      type: textProviderForm.value.type,
      provider_name: editingTextProvider.value || undefined,
      api_key: textProviderForm.value.api_key || undefined,
      base_url: textProviderForm.value.base_url,
      model: textProviderForm.value.model
    })
    if (result.success) {
      alert('✅ ' + result.message)
    }
  } catch (e: any) {
    alert('❌ 连接失败：' + (e.response?.data?.error || e.message))
  } finally {
    testingText.value = false
  }
}

// 测试图片服务商连接
async function testImageConnection() {
  testingImage.value = true
  try {
    const result = await testConnection({
      type: imageProviderForm.value.type,
      provider_name: editingImageProvider.value || undefined,
      api_key: imageProviderForm.value.api_key || undefined,
      base_url: imageProviderForm.value.base_url,
      model: imageProviderForm.value.model
    })
    if (result.success) {
      alert('✅ ' + result.message)
    }
  } catch (e: any) {
    alert('❌ 连接失败：' + (e.response?.data?.error || e.message))
  } finally {
    testingImage.value = false
  }
}

// 测试列表中的文本服务商
async function testTextProviderInList(name: string, provider: any) {
  try {
    const result = await testConnection({
      type: provider.type,
      provider_name: name,
      api_key: undefined,
      base_url: provider.base_url,
      model: provider.model
    })
    if (result.success) {
      alert('✅ ' + result.message)
    }
  } catch (e: any) {
    alert('❌ 连接失败：' + (e.response?.data?.error || e.message))
  }
}

// 测试列表中的图片服务商
async function testImageProviderInList(name: string, provider: any) {
  try {
    const result = await testConnection({
      type: provider.type,
      provider_name: name,
      api_key: undefined,
      base_url: provider.base_url,
      model: provider.model
    })
    if (result.success) {
      alert('✅ ' + result.message)
    }
  } catch (e: any) {
    alert('❌ 连接失败：' + (e.response?.data?.error || e.message))
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.settings-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Tabs Navigation */
.tabs-nav {
  display: flex;
  gap: 6px;
  padding: 4px;
  background: #F3F4F6;
  border-radius: 100px;
  width: fit-content;
  margin: 0 auto; /* 居中显示 */
  border: 1px solid var(--border-color);
}

.tab-btn {
  padding: 8px 24px;
  border-radius: 100px;
  border: none;
  background: transparent;
  color: var(--text-sub);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-btn:hover {
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.5);
}

.tab-btn.active {
  background: white;
  color: var(--primary);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Tab Content Animation */
.tab-content {
  animation: fadeIn 0.3s ease-out;
}

.card {
  background: white;
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(255, 255, 255, 0.5);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-fade);
  transform: translateY(-2px); /* 悬停轻微上浮 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px; /* 增加标题与内容的间距 */
}

.section-title {
  font-size: 22px; /* 增大标题字号 */
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.section-desc {
  font-size: 15px;
  color: var(--text-sub);
  margin: 0;
  line-height: 1.6;
}

/* Provider List Layout */
.provider-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.provider-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  transition: all 0.2s ease;
}

.provider-item:hover {
  border-color: var(--primary-fade);
  box-shadow: var(--shadow-sm);
  transform: translateY(-1px);
}

.provider-item.active {
  background: #FFF5F5; /* 极淡的红色背景 */
  border-color: var(--primary-fade);
  box-shadow: 0 2px 8px rgba(255, 36, 66, 0.05);
}

/* Info Section */
.provider-info {
  flex: 1;
  min-width: 0; /* 防止子元素溢出 */
  margin-right: 24px;
}

.provider-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.provider-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
}

.provider-type {
  font-size: 12px;
  padding: 2px 8px;
  background: #F3F4F6;
  border-radius: 100px;
  color: var(--text-secondary);
  font-weight: 500;
}

.provider-meta {
  display: flex;
  gap: 24px;
  color: var(--text-sub);
  font-size: 13px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 0; /* 允许文本截断 */
  max-width: 300px; /* 限制最大宽度 */
}

.meta-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta-text.code {
  font-family: 'Monaco', 'Menlo', monospace;
  color: var(--text-secondary);
}

/* Actions Section */
.provider-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.status-section {
  min-width: 80px;
  display: flex;
  justify-content: flex-end;
}

.status-text {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.status-text.active {
  color: #166534;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #166534;
  box-shadow: 0 0 0 2px #DCFCE7;
}

.action-divider {
  width: 1px;
  height: 20px;
  background: var(--border-color);
}

.icon-actions {
  display: flex;
  gap: 8px;
}

.btn-activate {
  padding: 6px 16px;
  border: 1px solid var(--border-color);
  border-radius: 100px;
  background: white;
  color: var(--text-main);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-activate:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--primary-fade);
  box-shadow: 0 2px 4px rgba(255, 36, 66, 0.1);
}

/* 按钮样式复用 */
.btn-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--text-sub);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #F3F4F6;
  color: var(--text-main);
}

.btn-icon.danger:hover {
  background: #FEF2F2;
  color: #DC2626;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5); /* 加深遮罩 */
  backdrop-filter: blur(8px); /* 增加模糊 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-content {
  background: white;
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 520px; /* 稍微加宽 */
  box-shadow: var(--shadow-xl);
  animation: slideUp 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.modal-header {
  padding: 32px 32px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.modal-header h3 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
  letter-spacing: -0.02em;
}

.close-btn {
  background: #F3F4F6;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 20px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #E5E7EB;
  color: var(--text-main);
  transform: rotate(90deg);
}

.modal-body {
  padding: 0 32px 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 10px;
}

/* Input Wrapper for Icons */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  color: var(--text-secondary);
  pointer-events: none;
  z-index: 1;
}

.input-wrapper .form-input,
.input-wrapper .form-select {
  padding-left: 44px; /* 为图标留出空间 */
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px 16px; /* 增加内边距 */
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 15px;
  color: var(--text-main);
  transition: all 0.2s;
  background: #F9FAFB;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--primary);
  background: white;
  box-shadow: 0 0 0 4px var(--primary-fade); /* 增大聚焦光晕 */
}

.input-wrapper .form-input:focus ~ .input-icon,
.input-wrapper .form-select:focus ~ .input-icon {
  color: var(--primary);
}

.form-hint {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 8px;
}

.modal-footer {
  padding: 24px 32px;
  background: #F9FAFB;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.btn {
  padding: 10px 24px; /* 增大按钮 */
  border-radius: 100px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.btn-primary {
  background: var(--primary);
  color: white;
  box-shadow: 0 4px 12px rgba(255, 36, 66, 0.25);
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 36, 66, 0.35);
}

.btn-small {
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  background: white;
  border: 1px solid var(--border-color);
  color: var(--text-main);
  border-radius: 100px;
  transition: all 0.2s;
}

.btn-small:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--primary-fade);
  transform: translateY(-1px);
}

/* Toggle Switch */
.toggle-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 4px 0;
}

.toggle-switch {
  width: 48px; /* 增大开关 */
  height: 28px;
  background: #E5E7EB;
  border-radius: 14px;
  position: relative;
  transition: all 0.3s;
}

.toggle-switch.active {
  background: var(--primary);
}

.toggle-slider {
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.toggle-switch.active .toggle-slider {
  transform: translateX(20px);
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
  color: var(--text-sub);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 按钮样式 */
.btn-small {
  padding: 6px 12px;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

/* 表单样式 */
.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #333;
  margin-bottom: 6px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  transition: all 0.2s;
  font-family: inherit;
  box-sizing: border-box;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-hint {
  display: block;
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

/* Toggle 开关样式 */
.toggle-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.toggle-switch {
  width: 44px;
  height: 24px;
  background: #d1d5db;
  border-radius: 12px;
  position: relative;
  transition: background 0.2s;
  flex-shrink: 0;
}

.toggle-switch.active {
  background: var(--primary);
}

.toggle-slider {
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.toggle-switch.active .toggle-slider {
  transform: translateX(20px);
}

/* 操作按钮区 */
.actions {
  margin-top: 32px;
  display: flex;
  justify-content: flex-end;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #666;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  box-sizing: border-box;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 480px;
  width: 100%;
  max-height: calc(100vh - 40px);
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #333;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 14px 20px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  flex-shrink: 0;
  background: white;
  border-radius: 0 0 12px 12px;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  display: inline-block;
  margin-right: 8px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .table-header,
  .table-row {
    grid-template-columns: 70px 1fr 80px;
  }

  .col-type,
  .col-model,
  .col-apikey {
    display: none;
  }

  .modal-overlay {
    padding: 16px;
    align-items: flex-end;
  }

  .modal-content {
    max-height: calc(100vh - 32px);
    border-radius: 16px 16px 0 0;
    max-width: 100%;
  }

  .modal-footer {
    border-radius: 0;
  }
}
</style>
