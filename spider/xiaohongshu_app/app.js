// 小红书风格小说阅读器 - 主应用逻辑

class NovelReader {
    constructor() {
        this.currentNovel = null;
        this.currentChapter = 0;
        this.readingSettings = {
            fontSize: 18,
            theme: 'light'
        };
        this.favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        this.readHistory = JSON.parse(localStorage.getItem('readHistory') || '[]');
        this.readingProgress = JSON.parse(localStorage.getItem('readingProgress') || '{}');
        
        this.init();
    }

    init() {
        this.loadSettings();
        this.renderNovels();
        this.hideLoading();
        this.setupEventListeners();
    }

    hideLoading() {
        setTimeout(() => {
            const loading = document.getElementById('loading');
            loading.classList.add('hidden');
            setTimeout(() => loading.style.display = 'none', 500);
        }, 1000);
    }

    setupEventListeners() {
        // 搜索功能
        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', this.debounce(this.handleSearchInput.bind(this), 300));

        // 键盘事件
        document.addEventListener('keydown', this.handleKeydown.bind(this));

        // 触摸事件（移动端）
        this.setupTouchEvents();
    }

    setupTouchEvents() {
        let startX = 0;
        let startY = 0;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            if (!e.changedTouches[0]) return;
            
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            const diffX = startX - endX;
            const diffY = startY - endY;

            // 只在阅读页面处理滑动
            if (document.getElementById('reading-page').classList.contains('active')) {
                if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                    if (diffX > 0) {
                        this.nextChapter(); // 向左滑动，下一章
                    } else {
                        this.previousChapter(); // 向右滑动，上一章
                    }
                }
            }
        });
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    handleKeydown(e) {
        if (document.getElementById('reading-page').classList.contains('active')) {
            switch(e.key) {
                case 'ArrowLeft':
                    this.previousChapter();
                    break;
                case 'ArrowRight':
                    this.nextChapter();
                    break;
                case 'Escape':
                    this.showDetail();
                    break;
            }
        }
    }

    renderNovels(novels = window.novelsData) {
        const grid = document.getElementById('novels-grid');
        grid.innerHTML = '';

        novels.forEach(novel => {
            const card = this.createNovelCard(novel);
            grid.appendChild(card);
        });
    }

    createNovelCard(novel) {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 col-xl-3';

        const isFavorite = this.favorites.includes(novel.id);
        const progress = this.readingProgress[novel.id] || { chapter: 0, progress: 0 };

        col.innerHTML = `
            <div class="novel-card" onclick="app.showNovelDetail(${novel.id})">
                <img src="${novel.cover}" class="card-img-top" alt="${novel.title}">
                <div class="card-body">
                    <h6 class="card-title">${novel.title}</h6>
                    <p class="card-text">${novel.description}</p>
                    <div class="novel-tags">
                        ${novel.tags.map(tag => `<span class="novel-tag">${tag}</span>`).join('')}
                    </div>
                    <div class="novel-stats">
                        <div class="novel-rating">
                            ${this.renderStars(novel.rating)}
                            <span class="ms-1">${novel.rating}</span>
                        </div>
                        <small class="text-muted">${novel.chapters}章</small>
                    </div>
                    ${progress.chapter > 0 ? `
                        <div class="mt-2">
                            <small class="text-primary">已读至第${progress.chapter}章</small>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;

        return col;
    }

    renderStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        let stars = '';

        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star"></i>';
        }
        if (hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        }
        for (let i = fullStars + (hasHalfStar ? 1 : 0); i < 5; i++) {
            stars += '<i class="far fa-star"></i>';
        }

        return stars;
    }

    showNovelDetail(novelId) {
        const novel = window.novelsData.find(n => n.id === novelId);
        if (!novel) return;

        this.currentNovel = novel;
        
        // 更新详情页内容
        document.getElementById('detail-cover').src = novel.cover;
        document.getElementById('detail-title').textContent = novel.title;
        document.getElementById('detail-author').textContent = `作者：${novel.author}`;
        document.getElementById('detail-description').textContent = novel.description;
        
        // 更新标签
        const tagsContainer = document.getElementById('detail-tags');
        tagsContainer.innerHTML = novel.tags.map(tag => 
            `<span class="badge bg-primary me-1">${tag}</span>`
        ).join('');

        // 更新收藏状态
        const favoriteIcon = document.getElementById('favorite-icon');
        const isFavorite = this.favorites.includes(novel.id);
        favoriteIcon.className = isFavorite ? 'fas fa-heart' : 'far fa-heart';

        // 渲染章节列表
        this.renderChaptersList(novel);

        // 显示详情页
        this.showPage('detail-page');
    }

    renderChaptersList(novel) {
        const chaptersList = document.getElementById('chapters-list');
        chaptersList.innerHTML = '';

        const progress = this.readingProgress[novel.id] || { chapter: 0 };

        novel.chapters_list.forEach((chapter, index) => {
            const chapterItem = document.createElement('div');
            chapterItem.className = `chapter-item ${index < progress.chapter ? 'read' : ''}`;
            chapterItem.textContent = chapter;
            chapterItem.onclick = () => this.startReading(index);
            chaptersList.appendChild(chapterItem);
        });
    }

    startReading(chapterIndex = 0) {
        if (!this.currentNovel) return;

        this.currentChapter = chapterIndex;
        this.loadChapter(chapterIndex);
        this.showPage('reading-page');
        
        // 更新阅读历史
        this.updateReadHistory(this.currentNovel.id);
        
        // 更新阅读进度
        this.updateReadingProgress(this.currentNovel.id, chapterIndex);
    }

    async loadChapter(chapterIndex) {
        const novel = this.currentNovel;
        const chapterTitle = novel.chapters_list[chapterIndex];
        
        // 更新标题
        document.getElementById('reading-title').textContent = novel.title;
        document.getElementById('chapter-info').textContent = 
            `${chapterIndex + 1}/${novel.chapters_list.length}`;

        // 更新按钮状态
        document.getElementById('prev-btn').disabled = chapterIndex === 0;
        document.getElementById('next-btn').disabled = chapterIndex === novel.chapters_list.length - 1;

        // 加载章节内容
        try {
            const content = await this.fetchChapterContent(novel.id, chapterIndex);
            document.getElementById('chapter-content').innerHTML = content;
            
            // 滚动到顶部
            window.scrollTo(0, 0);
            
            // 应用阅读设置
            this.applyReadingSettings();
            
        } catch (error) {
            console.error('加载章节失败:', error);
            this.showToast('章节加载失败，请重试');
        }
    }

    async fetchChapterContent(novelId, chapterIndex) {
        // 模拟从服务器获取章节内容
        // 实际应用中这里应该是API调用
        
        const novel = window.novelsData.find(n => n.id === novelId);
        const chapterTitle = novel.chapters_list[chapterIndex];
        
        // 生成模拟内容
        return `
            <h2>${chapterTitle}</h2>
            <p>这是${novel.title}的第${chapterIndex + 1}章内容。</p>
            <p>在这个充满奇幻色彩的世界中，主角正在经历着前所未有的冒险。每一个选择都可能改变命运的走向，每一次战斗都是成长的机会。</p>
            <p>随着故事的深入，更多的秘密将被揭开，更多的挑战等待着勇敢的冒险者。这不仅仅是一场个人的成长之旅，更是一个关于友情、勇气和信念的传奇故事。</p>
            <p>在接下来的章节中，我们将看到主角如何面对更大的挑战，如何在困境中找到希望，如何用自己的力量改变世界。</p>
            <p>故事还在继续，传奇永不落幕...</p>
        `;
    }

    previousChapter() {
        if (this.currentChapter > 0) {
            this.currentChapter--;
            this.loadChapter(this.currentChapter);
        }
    }

    nextChapter() {
        if (this.currentChapter < this.currentNovel.chapters_list.length - 1) {
            this.currentChapter++;
            this.loadChapter(this.currentChapter);
        }
    }

    toggleFavorite() {
        if (!this.currentNovel) return;

        const novelId = this.currentNovel.id;
        const index = this.favorites.indexOf(novelId);
        const favoriteIcon = document.getElementById('favorite-icon');

        if (index > -1) {
            this.favorites.splice(index, 1);
            favoriteIcon.className = 'far fa-heart';
            this.showToast('已取消收藏');
        } else {
            this.favorites.push(novelId);
            favoriteIcon.className = 'fas fa-heart';
            this.showToast('已添加到收藏');
        }

        localStorage.setItem('favorites', JSON.stringify(this.favorites));
    }

    updateReadHistory(novelId) {
        const index = this.readHistory.indexOf(novelId);
        if (index > -1) {
            this.readHistory.splice(index, 1);
        }
        this.readHistory.unshift(novelId);
        
        // 只保留最近20本
        if (this.readHistory.length > 20) {
            this.readHistory = this.readHistory.slice(0, 20);
        }
        
        localStorage.setItem('readHistory', JSON.stringify(this.readHistory));
    }

    updateReadingProgress(novelId, chapterIndex) {
        this.readingProgress[novelId] = {
            chapter: chapterIndex + 1,
            timestamp: Date.now()
        };
        localStorage.setItem('readingProgress', JSON.stringify(this.readingProgress));
    }

    // 搜索功能
    handleSearchInput(event) {
        const query = event.target.value.toLowerCase().trim();
        if (query === '') {
            this.renderNovels();
            return;
        }

        const filteredNovels = window.novelsData.filter(novel => 
            novel.title.toLowerCase().includes(query) ||
            novel.author.toLowerCase().includes(query) ||
            novel.description.toLowerCase().includes(query) ||
            novel.tags.some(tag => tag.toLowerCase().includes(query))
        );

        this.renderNovels(filteredNovels);
    }

    performSearch() {
        const query = document.getElementById('search-input').value;
        this.handleSearchInput({ target: { value: query } });
    }

    handleSearch(event) {
        if (event.key === 'Enter') {
            this.performSearch();
        }
    }

    // 分类筛选
    filterByCategory(category) {
        // 更新按钮状态
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');

        // 筛选小说
        let filteredNovels;
        if (category === 'all') {
            filteredNovels = window.novelsData;
        } else {
            filteredNovels = window.novelsData.filter(novel => 
                novel.tags.includes(category)
            );
        }

        this.renderNovels(filteredNovels);
    }

    // 页面切换
    showPage(pageId) {
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        document.getElementById(pageId).classList.add('active');

        // 更新底部导航状态
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        if (pageId === 'home-page') {
            document.querySelector('.nav-item').classList.add('active');
        }
    }

    showHome() {
        this.showPage('home-page');
    }

    showDetail() {
        this.showPage('detail-page');
    }

    // 阅读设置
    toggleReadingMenu() {
        const menu = document.getElementById('reading-menu');
        menu.classList.toggle('active');
    }

    adjustFontSize(delta) {
        this.readingSettings.fontSize = Math.max(14, Math.min(24, this.readingSettings.fontSize + delta));
        document.getElementById('font-size-display').textContent = this.readingSettings.fontSize + 'px';
        this.applyReadingSettings();
        this.saveSettings();
    }

    setReadingTheme(theme) {
        this.readingSettings.theme = theme;
        
        // 更新按钮状态
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-theme="${theme}"]`).classList.add('active');
        
        this.applyReadingSettings();
        this.saveSettings();
    }

    applyReadingSettings() {
        const content = document.getElementById('chapter-content');
        if (content) {
            content.style.fontSize = this.readingSettings.fontSize + 'px';
            
            // 移除所有主题类
            content.parentElement.classList.remove('theme-light', 'theme-dark', 'theme-sepia');
            // 添加当前主题类
            content.parentElement.classList.add(`theme-${this.readingSettings.theme}`);
        }
    }

    loadSettings() {
        const saved = localStorage.getItem('readingSettings');
        if (saved) {
            this.readingSettings = { ...this.readingSettings, ...JSON.parse(saved) };
        }
        
        // 更新UI
        document.getElementById('font-size-display').textContent = this.readingSettings.fontSize + 'px';
        document.querySelector(`[data-theme="${this.readingSettings.theme}"]`)?.classList.add('active');
    }

    saveSettings() {
        localStorage.setItem('readingSettings', JSON.stringify(this.readingSettings));
    }

    // 主题切换
    toggleTheme() {
        const body = document.body;
        const icon = document.getElementById('theme-icon');
        
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            icon.className = 'fas fa-moon';
            localStorage.setItem('theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
            icon.className = 'fas fa-sun';
            localStorage.setItem('theme', 'dark');
        }
    }

    // Toast提示
    showToast(message) {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');
        
        toastMessage.textContent = message;
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    // 收藏页面
    showFavorites() {
        const favoriteNovels = window.novelsData.filter(novel =>
            this.favorites.includes(novel.id)
        );

        if (favoriteNovels.length === 0) {
            this.showToast('还没有收藏任何小说');
            return;
        }

        // 创建收藏页面
        this.createFavoritesPage(favoriteNovels);
        this.showPage('favorites-page');
    }

    createFavoritesPage(novels) {
        let favoritesPage = document.getElementById('favorites-page');
        if (!favoritesPage) {
            favoritesPage = document.createElement('div');
            favoritesPage.id = 'favorites-page';
            favoritesPage.className = 'page';
            document.querySelector('main').appendChild(favoritesPage);
        }

        favoritesPage.innerHTML = `
            <div class="detail-header">
                <div class="container-fluid">
                    <div class="d-flex justify-content-between align-items-center">
                        <button class="btn btn-link text-white" onclick="app.showHome()">
                            <i class="fas fa-arrow-left"></i> 返回
                        </button>
                        <span class="text-white fw-bold">我的收藏</span>
                        <button class="btn btn-link text-white" onclick="app.clearAllFavorites()">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="container">
                <div class="row" id="favorites-grid">
                    ${novels.map(novel => this.createFavoriteCard(novel)).join('')}
                </div>
            </div>
        `;
    }

    createFavoriteCard(novel) {
        const progress = this.readingProgress[novel.id] || { chapter: 0 };
        return `
            <div class="col-md-6 col-lg-4 col-xl-3 mb-3">
                <div class="novel-card" onclick="app.showNovelDetail(${novel.id})">
                    <img src="${novel.cover}" class="card-img-top" alt="${novel.title}">
                    <div class="card-body">
                        <h6 class="card-title">${novel.title}</h6>
                        <p class="card-text">${novel.description.substring(0, 50)}...</p>
                        ${progress.chapter > 0 ? `
                            <div class="progress mb-2">
                                <div class="progress-bar bg-primary" style="width: ${(progress.chapter / novel.chapters_list.length * 100).toFixed(1)}%"></div>
                            </div>
                            <small class="text-primary">已读 ${progress.chapter}/${novel.chapters_list.length} 章</small>
                        ` : ''}
                        <div class="mt-2">
                            <button class="btn btn-sm btn-outline-danger" onclick="event.stopPropagation(); app.removeFavorite(${novel.id})">
                                <i class="fas fa-heart-broken"></i> 取消收藏
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    removeFavorite(novelId) {
        const index = this.favorites.indexOf(novelId);
        if (index > -1) {
            this.favorites.splice(index, 1);
            localStorage.setItem('favorites', JSON.stringify(this.favorites));
            this.showToast('已取消收藏');

            // 刷新收藏页面
            const favoriteNovels = window.novelsData.filter(novel =>
                this.favorites.includes(novel.id)
            );
            if (favoriteNovels.length > 0) {
                this.createFavoritesPage(favoriteNovels);
            } else {
                this.showHome();
            }
        }
    }

    clearAllFavorites() {
        if (confirm('确定要清空所有收藏吗？')) {
            this.favorites = [];
            localStorage.setItem('favorites', JSON.stringify(this.favorites));
            this.showToast('已清空收藏');
            this.showHome();
        }
    }

    // 历史记录页面
    showHistory() {
        const historyNovels = this.readHistory.map(novelId =>
            window.novelsData.find(novel => novel.id === novelId)
        ).filter(novel => novel);

        if (historyNovels.length === 0) {
            this.showToast('还没有阅读历史');
            return;
        }

        this.createHistoryPage(historyNovels);
        this.showPage('history-page');
    }

    createHistoryPage(novels) {
        let historyPage = document.getElementById('history-page');
        if (!historyPage) {
            historyPage = document.createElement('div');
            historyPage.id = 'history-page';
            historyPage.className = 'page';
            document.querySelector('main').appendChild(historyPage);
        }

        historyPage.innerHTML = `
            <div class="detail-header">
                <div class="container-fluid">
                    <div class="d-flex justify-content-between align-items-center">
                        <button class="btn btn-link text-white" onclick="app.showHome()">
                            <i class="fas fa-arrow-left"></i> 返回
                        </button>
                        <span class="text-white fw-bold">阅读历史</span>
                        <button class="btn btn-link text-white" onclick="app.clearHistory()">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="container">
                <div class="history-list">
                    ${novels.map(novel => this.createHistoryItem(novel)).join('')}
                </div>
            </div>
        `;
    }

    createHistoryItem(novel) {
        const progress = this.readingProgress[novel.id] || { chapter: 0, timestamp: 0 };
        const lastRead = progress.timestamp ? new Date(progress.timestamp).toLocaleDateString() : '未知';

        return `
            <div class="history-item" onclick="app.showNovelDetail(${novel.id})">
                <div class="row align-items-center">
                    <div class="col-3">
                        <img src="${novel.cover}" class="img-fluid rounded" alt="${novel.title}">
                    </div>
                    <div class="col-9">
                        <h6 class="mb-1">${novel.title}</h6>
                        <p class="text-muted small mb-1">${novel.author}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-primary">
                                ${progress.chapter > 0 ? `读到第${progress.chapter}章` : '未开始阅读'}
                            </small>
                            <small class="text-muted">${lastRead}</small>
                        </div>
                        <div class="progress mt-1" style="height: 3px;">
                            <div class="progress-bar bg-primary" style="width: ${(progress.chapter / novel.chapters_list.length * 100).toFixed(1)}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    clearHistory() {
        if (confirm('确定要清空阅读历史吗？')) {
            this.readHistory = [];
            localStorage.setItem('readHistory', JSON.stringify(this.readHistory));
            this.showToast('已清空历史记录');
            this.showHome();
        }
    }

    // 设置页面
    showSettings() {
        this.createSettingsPage();
        this.showPage('settings-page');
    }

    createSettingsPage() {
        let settingsPage = document.getElementById('settings-page');
        if (!settingsPage) {
            settingsPage = document.createElement('div');
            settingsPage.id = 'settings-page';
            settingsPage.className = 'page';
            document.querySelector('main').appendChild(settingsPage);
        }

        const stats = this.getReadingStats();

        settingsPage.innerHTML = `
            <div class="detail-header">
                <div class="container-fluid">
                    <div class="d-flex justify-content-between align-items-center">
                        <button class="btn btn-link text-white" onclick="app.showHome()">
                            <i class="fas fa-arrow-left"></i> 返回
                        </button>
                        <span class="text-white fw-bold">个人中心</span>
                        <div></div>
                    </div>
                </div>
            </div>
            <div class="container">
                <!-- 阅读统计 -->
                <div class="stats-card mb-4">
                    <h5 class="mb-3"><i class="fas fa-chart-bar me-2"></i>阅读统计</h5>
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="stat-item">
                                <div class="stat-number">${stats.totalBooks}</div>
                                <div class="stat-label">阅读书籍</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="stat-item">
                                <div class="stat-number">${stats.totalChapters}</div>
                                <div class="stat-label">阅读章节</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="stat-item">
                                <div class="stat-number">${stats.favoriteCount}</div>
                                <div class="stat-label">收藏数量</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 设置选项 -->
                <div class="settings-card">
                    <h5 class="mb-3"><i class="fas fa-cog me-2"></i>应用设置</h5>

                    <div class="setting-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="setting-title">夜间模式</div>
                                <div class="setting-desc">保护眼睛，减少蓝光</div>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" id="darkModeSwitch"
                                       ${document.body.getAttribute('data-theme') === 'dark' ? 'checked' : ''}
                                       onchange="app.toggleTheme()">
                            </div>
                        </div>
                    </div>

                    <div class="setting-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="setting-title">自动保存进度</div>
                                <div class="setting-desc">自动记录阅读位置</div>
                            </div>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" checked disabled>
                            </div>
                        </div>
                    </div>

                    <div class="setting-item">
                        <div class="setting-title">清除数据</div>
                        <div class="setting-desc">清除所有本地数据</div>
                        <button class="btn btn-outline-danger btn-sm mt-2" onclick="app.clearAllData()">
                            <i class="fas fa-trash me-1"></i>清除所有数据
                        </button>
                    </div>

                    <div class="setting-item">
                        <div class="setting-title">关于应用</div>
                        <div class="setting-desc">版本 1.0.0</div>
                        <div class="mt-2">
                            <small class="text-muted">
                                小红书风格小说阅读器<br>
                                支持PWA，可安装到桌面
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getReadingStats() {
        const totalBooks = this.readHistory.length;
        const totalChapters = Object.values(this.readingProgress)
            .reduce((sum, progress) => sum + (progress.chapter || 0), 0);
        const favoriteCount = this.favorites.length;

        return {
            totalBooks,
            totalChapters,
            favoriteCount
        };
    }

    clearAllData() {
        if (confirm('确定要清除所有数据吗？这将删除收藏、历史记录和阅读进度，且无法恢复。')) {
            localStorage.clear();
            this.favorites = [];
            this.readHistory = [];
            this.readingProgress = {};
            this.readingSettings = { fontSize: 18, theme: 'light' };
            this.showToast('所有数据已清除');
            this.showHome();
        }
    }

    showChapterList() {
        this.toggleReadingMenu();
        this.showDetail();
    }
}

// 全局函数（供HTML调用）
let app;

window.addEventListener('DOMContentLoaded', () => {
    app = new NovelReader();
});

// 导出全局函数
window.showHome = () => app.showHome();
window.showDetail = () => app.showDetail();
window.filterByCategory = (category) => app.filterByCategory(category);
window.performSearch = () => app.performSearch();
window.handleSearch = (event) => app.handleSearch(event);
window.toggleTheme = () => app.toggleTheme();
window.toggleFavorite = () => app.toggleFavorite();
window.startReading = () => app.startReading();
window.previousChapter = () => app.previousChapter();
window.nextChapter = () => app.nextChapter();
window.toggleReadingMenu = () => app.toggleReadingMenu();
window.adjustFontSize = (delta) => app.adjustFontSize(delta);
window.setReadingTheme = (theme) => app.setReadingTheme(theme);
window.showChapterList = () => app.showChapterList();
window.showFavorites = () => app.showFavorites();
window.showHistory = () => app.showHistory();
window.showSettings = () => app.showSettings();
