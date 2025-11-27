<template>
  <div class="container" style="max-width: 100%;">
    <div class="page-header" style="max-width: 1200px; margin: 0 auto 30px auto;">
      <div>
        <h1 class="page-title">编辑大纲</h1>
        <p class="page-subtitle">调整页面顺序，修改文案，打造完美内容</p>
      </div>
      <div style="display: flex; gap: 12px;">
        <button class="btn btn-secondary" @click="goBack" style="background: white; border: 1px solid var(--border-color);">
          上一步
        </button>
        <button class="btn btn-primary" @click="startGeneration">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"></path><line x1="16" y1="8" x2="2" y2="22"></line><line x1="17.5" y1="15" x2="9" y2="15"></line></svg>
          开始生成图片
        </button>
      </div>
    </div>

    <div class="outline-grid">
      <div 
        v-for="(page, idx) in store.outline.pages" 
        :key="page.index"
        class="card outline-card"
        :draggable="true"
        @dragstart="onDragStart($event, idx)"
        @dragover.prevent="onDragOver($event, idx)"
        @drop="onDrop($event, idx)"
        :class="{ 'dragging-over': dragOverIndex === idx }"
      >
        <!-- 拖拽手柄 (改为右上角或更加隐蔽) -->
        <div class="card-top-bar">
          <div class="page-info">
             <span class="page-number">P{{ idx + 1 }}</span>
             <span class="page-type" :class="page.type">{{ getPageTypeName(page.type) }}</span>
          </div>
          
          <div class="card-controls">
            <div class="drag-handle" title="拖拽排序">
               <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="12" r="1"></circle><circle cx="9" cy="5" r="1"></circle><circle cx="9" cy="19" r="1"></circle><circle cx="15" cy="12" r="1"></circle><circle cx="15" cy="5" r="1"></circle><circle cx="15" cy="19" r="1"></circle></svg>
            </div>
            <button class="icon-btn" @click="deletePage(idx)" title="删除此页">
               <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>
        </div>

        <textarea
          v-model="page.content"
          class="textarea-paper"
          placeholder="在此输入文案..."
          @input="store.updatePage(page.index, page.content)"
        />
        
        <div class="word-count">{{ page.content.length }} 字</div>
      </div>

      <!-- 添加按钮卡片 -->
      <div class="card add-card-dashed" @click="addPage('content')">
        <div class="add-content">
          <div class="add-icon">+</div>
          <span>添加页面</span>
        </div>
      </div>
    </div>
    
    <div style="height: 100px;"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useGeneratorStore } from '../stores/generator'

const router = useRouter()
const store = useGeneratorStore()

const dragOverIndex = ref<number | null>(null)
const draggedIndex = ref<number | null>(null)

const getPageTypeName = (type: string) => {
  const names = {
    cover: '封面',
    content: '内容',
    summary: '总结'
  }
  return names[type as keyof typeof names] || '内容'
}

// 拖拽逻辑
const onDragStart = (e: DragEvent, index: number) => {
  draggedIndex.value = index
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.dropEffect = 'move'
  }
}

const onDragOver = (e: DragEvent, index: number) => {
  if (draggedIndex.value === index) return
  dragOverIndex.value = index
}

const onDrop = (e: DragEvent, index: number) => {
  dragOverIndex.value = null
  if (draggedIndex.value !== null && draggedIndex.value !== index) {
    store.movePage(draggedIndex.value, index)
  }
  draggedIndex.value = null
}

const deletePage = (index: number) => {
  if (confirm('确定要删除这一页吗？')) {
    store.deletePage(index)
  }
}

const addPage = (type: 'cover' | 'content' | 'summary') => {
  store.addPage(type, '')
  // 滚动到底部
  nextTick(() => {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
  })
}

const goBack = () => {
  router.push('/')
}

const startGeneration = () => {
  router.push('/generate')
}
</script>

<style scoped>
/* 网格布局 */
.outline-grid {
  display: grid;
  /* 响应式列：最小宽度 300px，自动填充 */
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.outline-card {
  display: flex;
  flex-direction: column;
  padding: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  background: white;
  box-shadow: var(--shadow-sm);
  min-height: 380px; 
  position: relative;
}

.outline-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-fade);
  z-index: 10;
}

.outline-card.dragging-over {
  border: 2px dashed var(--primary);
  background: var(--primary-light);
  transform: scale(1.02);
}

/* 顶部栏 */
.card-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.page-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-number {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-placeholder);
  font-family: 'Monaco', monospace;
}

.page-type {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.page-type.cover { color: #FF4D4F; background: #FFF1F0; }
.page-type.content { color: var(--text-sub); background: #F3F4F6; }
.page-type.summary { color: #52C41A; background: #F6FFED; }

.card-controls {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}
.outline-card:hover .card-controls { opacity: 1; }

.drag-handle {
  cursor: grab;
  padding: 4px;
  border-radius: 4px;
  color: var(--text-placeholder);
  transition: all 0.2s;
}
.drag-handle:hover { 
  background: #F3F4F6; 
  color: var(--text-main);
}
.drag-handle:active { cursor: grabbing; }

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-placeholder);
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}
.icon-btn:hover { 
  background: #FEF2F2;
  color: #DC2626; 
}

/* 文本区域 - 核心 */
.textarea-paper {
  flex: 1; /* 占据剩余空间 */
  width: 100%;
  border: none;
  background: transparent;
  padding: 0;
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-main);
  resize: none;
  font-family: inherit;
  margin-bottom: 16px;
}

.textarea-paper:focus {
  outline: none;
}

.textarea-paper::placeholder {
  color: var(--text-placeholder);
}

.word-count {
  text-align: right;
  font-size: 12px;
  color: var(--text-placeholder);
  margin-top: auto;
  font-variant-numeric: tabular-nums;
}

/* 添加卡片 */
.add-card-dashed {
  border: 2px dashed var(--border-color);
  background: transparent;
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  min-height: 380px;
  color: var(--text-placeholder);
  transition: all 0.3s;
  border-radius: var(--radius-lg);
}

.add-card-dashed:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--primary-fade);
  transform: translateY(-4px);
}

.add-content {
  text-align: center;
}

.add-icon {
  font-size: 40px;
  font-weight: 300;
  margin-bottom: 12px;
  line-height: 1;
}

.add-content span {
  font-size: 14px;
  font-weight: 500;
}
</style>
