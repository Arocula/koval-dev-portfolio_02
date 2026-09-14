import React, { useState } from 'react';

function FlaskDemo({ darkMode }) {
  const [activeTab, setActiveTab] = useState('preview');
  const [iframeLoaded, setIframeLoaded] = useState(false);

  return (
    <div className={`flask-demo ${darkMode ? 'dark' : ''}`}>
      <div className="flask-demo-header">
        <div className="flask-status">
          <span className="status-dot green"></span>
          Flask сервер запущен
        </div>
        <div className="flask-stats">
          <span>⚡ Flask 3.0</span>
          <span>🗄️ SQLite</span>
          <span>💰 от 50 000 ₽</span>
        </div>
      </div>

      <div className="flask-tabs">
        <button 
          className={`flask-tab ${activeTab === 'preview' ? 'active' : ''}`}
          onClick={() => setActiveTab('preview')}
        >
          🖥️ Демо сайта
        </button>
        <button 
          className={`flask-tab ${activeTab === 'info' ? 'active' : ''}`}
          onClick={() => setActiveTab('info')}
        >
          📋 О проекте
        </button>
        <button 
          className={`flask-tab ${activeTab === 'code' ? 'active' : ''}`}
          onClick={() => setActiveTab('code')}
        >
          💻 Код
        </button>
      </div>

      <div className="flask-demo-content">
        {activeTab === 'preview' && (
          <div className="flask-preview">
            {!iframeLoaded && (
              <div className="iframe-loader">
                <div className="loader-spinner"></div>
                <p>Загрузка Flask-приложения...</p>
              </div>
            )}
            <iframe
              src="http://localhost:5000"
              className="flask-iframe"
              onLoad={() => setIframeLoaded(true)}
              style={{ display: iframeLoaded ? 'block' : 'none' }}
              title="Flask Demo"
            />
            <div className="flask-preview-actions">
              <a href="http://localhost:5000" target="_blank" rel="noopener noreferrer" className="flask-btn primary">
                🔗 Открыть в новой вкладке
              </a>
              <a href="http://localhost:5000/admin/login" target="_blank" rel="noopener noreferrer" className="flask-btn secondary">
                🔐 Админка (admin/admin123)
              </a>
            </div>
          </div>
        )}

        {activeTab === 'info' && (
          <div className="flask-info-content">
            <h3>📊 О проекте "БетонПартнер"</h3>
            
            <div className="info-grid">
              <div className="info-block">
                <h4>Технологии</h4>
                <ul>
                  <li><strong>Flask 3.0.3</strong> — микрофреймворк</li>
                  <li><strong>SQLAlchemy</strong> — ORM для работы с БД</li>
                  <li><strong>SQLite</strong> — легкая база данных</li>
                  <li><strong>Jinja2</strong> — шаблонизатор</li>
                  <li><strong>Bootstrap 5</strong> — CSS-фреймворк</li>
                </ul>
              </div>

              <div className="info-block">
                <h4>Бюджет</h4>
                <ul>
                  <li><strong>Разработка:</strong> от 50 000 ₽</li>
                  <li><strong>Хостинг:</strong> от 300 ₽/мес</li>
                  <li><strong>База данных:</strong> бесплатно (SQLite)</li>
                  <li><strong>Домен:</strong> от 500 ₽/год</li>
                  <li><strong>Итого в год:</strong> ~4 000 ₽</li>
                </ul>
              </div>

              <div className="info-block">
                <h4>Функционал</h4>
                <ul>
                  <li>✅ Главная страница</li>
                  <li>✅ Прайс-лист с ценами</li>
                  <li>✅ Админ-панель (CRUD)</li>
                  <li>✅ Контакты и карта</li>
                  <li>✅ Информационные страницы</li>
                  <li>✅ Адаптивный дизайн</li>
                </ul>
              </div>

              <div className="info-block">
                <h4>Для кого</h4>
                <ul>
                  <li>🏗️ Строительные компании</li>
                  <li>🏠 Частные застройщики</li>
                  <li>🏢 Производственные предприятия</li>
                  <li>🚚 Поставщики материалов</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'code' && (
          <div className="flask-code-content">
            <h3>📄 Структура проекта</h3>
            <pre className="code-block">
{`flask-demo/
├── app.py                 # Основной файл (400+ строк)
├── requirements.txt       # Зависимости
├── templates/
│   ├── base.html          # Базовый шаблон
│   ├── index.html         # Главная страница
│   ├── about.html         # О заводе
│   ├── contacts.html      # Контакты
│   ├── price.html         # Прайс-лист
│   ├── privacy.html       # Политика
│   └── admin/
│       ├── login.html     # Вход в админку
│       └── dashboard.html # Панель управления
└── static/
    └── css/
        └── style.css      # Стили (400+ строк)`}
            </pre>
            
            <div className="code-features">
              <div className="code-feature">
                <span>🗄️</span>
                <div>
                  <h4>Модели данных</h4>
                  <p>ConcretePrice, MortarPrice, FineConcretePrice, ZBIPrice</p>
                </div>
              </div>
              <div className="code-feature">
                <span>🔐</span>
                <div>
                  <h4>Админ-панель</h4>
                  <p>Полный CRUD для всех товаров с защитой паролем</p>
                </div>
              </div>
              <div className="code-feature">
                <span>📱</span>
                <div>
                  <h4>Адаптивность</h4>
                  <p>Работает на всех устройствах от телефона до ПК</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FlaskDemo;