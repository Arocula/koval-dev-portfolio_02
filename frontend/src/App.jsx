import { useEffect, useState } from 'react';
import {
  ImBriefcase,
  ImCart,
  ImCog,
  ImContrast,
  ImDatabase,
  ImFire,
  ImHome,
  ImLoop,
  ImPhone,
  ImQuestion,
  ImSun,
  ImUser,
} from 'react-icons/im';

import HomePage from './components/HomePage';
import FlaskDemo from './components/FlaskDemo';

const BIOS_SECTIONS = [
  { id: 'cpu', label: 'CPU', icon: ImCog },
  { id: 'memory', label: 'Memory', icon: ImDatabase },
  { id: 'storage', label: 'Storage', icon: ImDatabase },
  { id: 'fan', label: 'Fan Info', icon: ImLoop },
  { id: 'help', label: 'Help', icon: ImQuestion },
];

const MENU_ITEMS = [
  { id: 'home', label: 'HOME', icon: ImHome },
  { id: 'bios', label: 'BIOS', icon: ImCog },
  { id: 'projects', label: 'PROJECTS', icon: ImBriefcase },
  { id: 'flask', label: 'FLASK DEMO', icon: ImFire },
  { id: 'price', label: 'PRICING', icon: ImCart },
  { id: 'about', label: 'ABOUT', icon: ImUser },
  { id: 'contacts', label: 'CONTACTS', icon: ImPhone },
];

const CONTENT_SECTIONS = {
  projects: {
    title: 'Проекты',
    description: 'Разрабатываем сайты и веб-сервисы под бизнес-задачи: от первого прототипа до запуска и поддержки.',
    cards: [
      { title: 'Продающие лендинги', text: 'Структура, дизайн, адаптивная верстка, аналитика и формы заявок.', tags: ['React', 'UX/UI', 'Аналитика'] },
      { title: 'Корпоративные сайты', text: 'Многостраничные проекты с удобным управлением контентом и интеграциями.', tags: ['FastAPI', 'CMS', 'CRM'] },
      { title: 'Веб-сервисы', text: 'Личные кабинеты, каталоги, калькуляторы и автоматизация внутренних процессов.', tags: ['API', 'Базы данных', 'Интеграции'] },
    ],
  },
  price: {
    title: 'Форматы работы',
    description: 'Точная стоимость определяется после короткого опроса и обсуждения требований.',
    cards: [
      { title: 'Старт', text: 'Лендинг или компактный сайт для проверки идеи и быстрого запуска.', tags: ['От 2 недель', 'Адаптивность'] },
      { title: 'Бизнес', text: 'Корпоративный сайт, каталог, формы и подключение внешних сервисов.', tags: ['Интеграции', 'SEO-база'] },
      { title: 'Индивидуально', text: 'Веб-приложение со сложной логикой, API и личными кабинетами.', tags: ['Проектирование', 'Поддержка'] },
    ],
  },
  about: {
    title: 'О подходе',
    description: 'KOVAL_DEV — разработка без лишней бюрократии: понятные этапы, прозрачный прогресс и рабочий результат.',
    cards: [
      { title: 'Сначала задача', text: 'Разбираемся в целях проекта и предлагаем решение, а не набор случайных функций.', tags: ['Аналитика', 'Прототип'] },
      { title: 'Чистая разработка', text: 'Структурированный код, понятный запуск и возможность развивать проект дальше.', tags: ['React', 'FastAPI'] },
      { title: 'После релиза', text: 'Помогаем с обновлениями, исправлениями и развитием продукта.', tags: ['Поддержка', 'Развитие'] },
    ],
  },
  contacts: {
    title: 'Обсудим проект',
    description: 'Пройдите короткий опрос на главной странице. Ответы сразу попадут в заявку и помогут быстрее подготовить предложение.',
    cards: [
      { title: '10 вопросов', text: 'Опрос занимает несколько минут и фиксирует основные требования.', tags: ['Быстро', 'Без регистрации'] },
      { title: 'Ответ в течение 24 часов', text: 'Свяжемся по указанному email или телефону и уточним детали.', tags: ['Email', 'Телефон'] },
      { title: 'Без потери заявки', text: 'Backend сохраняет данные локально даже при временном сбое почтового сервера.', tags: ['Надежность', 'FastAPI'] },
    ],
  },
  flask: {
    title: 'Flask — Бюджетный микросервис',
    description: 'Самый экономичный вариант для небольших проектов. Простота, скорость и минимальные затраты на хостинг.',
    cards: [
      { 
        title: 'Минимальный стек', 
        text: 'Flask + SQLite + Jinja2 — лёгкое решение без лишних зависимостей. Идеально для стартапов и MVP.', 
        tags: ['Flask', 'SQLite', 'Jinja2'] 
      },
      { 
        title: 'Бюджетное решение', 
        text: 'Стоимость разработки от 50 000 ₽. Хостинг от 300 ₽/мес. Это самый доступный вариант на рынке.', 
        tags: ['Экономия', 'Быстрый старт'] 
      },
      { 
        title: 'Живой пример', 
        text: 'Ниже вы можете взаимодействовать с работающим Flask-приложением. Кликайте и смотрите!', 
        tags: ['Демо', 'Интерактив'] 
      },
    ],
  },
};

function InfoSection({ sectionId, darkMode }) {
  const section = CONTENT_SECTIONS[sectionId];
  if (!section) return null;

  // Показываем FlaskDemo для раздела flask
  if (sectionId === 'flask') {
    return (
      <section className={`content-section ${darkMode ? 'dark' : ''}`}>
        <div className="section-shell">
          <p className="section-kicker">KOVAL_DEV</p>
          <h2>{section.title}</h2>
          <p className="section-description">{section.description}</p>
          <div className="section-card-grid">
            {section.cards.map((card) => (
              <article className="section-card" key={card.title}>
                <h3>{card.title}</h3>
                <p>{card.text}</p>
                <div className="section-tags">
                  {card.tags.map((tag) => <span key={tag}>{tag}</span>)}
                </div>
              </article>
            ))}
          </div>
          <FlaskDemo darkMode={darkMode} />
        </div>
      </section>
    );
  }

  return (
    <section className={`content-section ${darkMode ? 'dark' : ''}`}>
      <div className="section-shell">
        <p className="section-kicker">KOVAL_DEV</p>
        <h2>{section.title}</h2>
        <p className="section-description">{section.description}</p>
        <div className="section-card-grid">
          {section.cards.map((card) => (
            <article className="section-card" key={card.title}>
              <h3>{card.title}</h3>
              <p>{card.text}</p>
              <div className="section-tags">
                {card.tags.map((tag) => <span key={tag}>{tag}</span>)}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('portfolio-theme') !== 'light');
  const [biosSection, setBiosSection] = useState('cpu');

  const [cpuTemp, setCpuTemp] = useState(29);
  const [mbTemp, setMbTemp] = useState(31);
  const [cpuFreq, setCpuFreq] = useState(4.0);
  const [cpuLoad, setCpuLoad] = useState(45);
  const [ramUsage, setRamUsage] = useState(62);
  const [fanSpeed, setFanSpeed] = useState(1200);
  const [time, setTime] = useState(new Date());

  const [fastBoot, setFastBoot] = useState(true);
  const [ahci, setAhci] = useState(true);
  const [hdAudio, setHdAudio] = useState(true);

  useEffect(() => {
    document.body.classList.toggle('dark', darkMode);
    localStorage.setItem('portfolio-theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  useEffect(() => {
    if (activeTab !== 'bios') return undefined;

    const sectionInterval = window.setInterval(() => {
      setBiosSection((currentSection) => {
        const currentIndex = BIOS_SECTIONS.findIndex((section) => section.id === currentSection);
        const nextIndex = (currentIndex + 1) % BIOS_SECTIONS.length;
        return BIOS_SECTIONS[nextIndex].id;
      });
    }, 8000);

    return () => window.clearInterval(sectionInterval);
  }, [activeTab]);

  useEffect(() => {
    if (activeTab !== 'bios') return undefined;

    const toggleInterval = window.setInterval(() => {
      const randomValue = Math.random();
      if (randomValue < 0.33) setFastBoot((value) => !value);
      else if (randomValue < 0.66) setAhci((value) => !value);
      else setHdAudio((value) => !value);
    }, 5000);

    return () => window.clearInterval(toggleInterval);
  }, [activeTab]);

  useEffect(() => {
    if (activeTab !== 'bios') return undefined;

    const metricsInterval = window.setInterval(() => {
      setTime(new Date());
      setCpuTemp((value) => Math.max(25, Math.min(85, value + (Math.random() - 0.5) * 3)));
      setMbTemp((value) => Math.max(25, Math.min(60, value + (Math.random() - 0.5) * 2)));
      setCpuFreq(3.8 + Math.random() * 0.4);
      setCpuLoad(Math.floor(Math.random() * 100));
      setRamUsage(Math.floor(Math.random() * 40) + 40);
      setFanSpeed(Math.floor(800 + Math.random() * 800));
    }, 1500);

    return () => window.clearInterval(metricsInterval);
  }, [activeTab]);

  const renderBiosContent = () => {
    switch (biosSection) {
      case 'cpu':
        return (
          <div className="bios-main-grid">
            <div className="bios-big-stat">
              <div className="stat-label">CPU Frequency:</div>
              <div className="stat-value">{cpuFreq.toFixed(2)} <span className="stat-unit">GHz</span></div>
            </div>
            <div className="bios-details">
              <div className="detail-row"><span>CPU Base Clock:</span><span>100.00MHz</span></div>
              <div className="detail-row"><span>CPU Ratio:</span><span>40</span></div>
              <div className="detail-row"><span>Core Number:</span><span>8</span></div>
              <div className="detail-row"><span>CPU Core Voltage:</span><span>1.192V</span></div>
              <div className="detail-row"><span>Intel Turbo Boost:</span><span className="yes">YES</span></div>
              <div className="detail-row"><span>Hyper-Threading:</span><span className="yes">YES</span></div>
              <div className="detail-row"><span>Virtualization:</span><span className="yes">Enabled</span></div>
              <div className="detail-row"><span>Instruction Set:</span><span>MMX, SSE, SSE2, SSE3, SSE4</span></div>
            </div>
          </div>
        );
      case 'memory':
        return (
          <div className="bios-main-grid">
            <div className="bios-big-stat">
              <div className="stat-label">DDR Speed:</div>
              <div className="stat-value">{2133 + Math.floor(Math.random() * 100)} <span className="stat-unit">MHz</span></div>
            </div>
            <div className="bios-details">
              <div className="detail-row"><span>Memory Size:</span><span>16384MB</span></div>
              <div className="detail-row"><span>Memory Type:</span><span>DDR4</span></div>
              <div className="detail-row"><span>DDR Voltage:</span><span>1.360V</span></div>
              <div className="detail-row"><span>CAS Latency:</span><span>15</span></div>
              <div className="detail-row"><span>tRCD:</span><span>15</span></div>
              <div className="detail-row"><span>tRP:</span><span>15</span></div>
              <div className="detail-row"><span>tRAS:</span><span>36</span></div>
              <div className="detail-row"><span>XMP Profile:</span><span className="yes">Enabled</span></div>
            </div>
          </div>
        );
      case 'storage':
        return (
          <div className="bios-main-grid">
            <div className="bios-big-stat">
              <div className="stat-label">Storage:</div>
              <div className="stat-value">NVMe <span className="stat-unit">SSD</span></div>
            </div>
            <div className="bios-details">
              <div className="detail-row"><span>Drive 1:</span><span>Samsung 980 Pro 1TB</span></div>
              <div className="detail-row"><span>Interface:</span><span>PCIe 4.0 x4</span></div>
              <div className="detail-row"><span>Read Speed:</span><span>7000 MB/s</span></div>
              <div className="detail-row"><span>Write Speed:</span><span>5000 MB/s</span></div>
              <div className="detail-row"><span>Temperature:</span><span className="ok">42°C</span></div>
              <div className="detail-row"><span>Health:</span><span className="yes">98%</span></div>
              <div className="detail-row"><span>AHCI Mode:</span><span className="yes">Enabled</span></div>
              <div className="detail-row"><span>SMART Status:</span><span className="yes">Good</span></div>
            </div>
          </div>
        );
      case 'fan':
        return (
          <div className="bios-main-grid">
            <div className="bios-big-stat">
              <div className="stat-label">Fan Speed:</div>
              <div className="stat-value">{fanSpeed} <span className="stat-unit">RPM</span></div>
            </div>
            <div className="bios-details">
              <div className="detail-row"><span>CPU Fan:</span><span>{fanSpeed} RPM</span></div>
              <div className="detail-row"><span>System Fan 1:</span><span>{fanSpeed - 200} RPM</span></div>
              <div className="detail-row"><span>System Fan 2:</span><span>{fanSpeed - 150} RPM</span></div>
              <div className="detail-row"><span>GPU Fan:</span><span>{fanSpeed + 100} RPM</span></div>
              <div className="detail-row"><span>Fan Control:</span><span className="yes">Smart Fan</span></div>
              <div className="detail-row"><span>Fan Curve:</span><span>Custom</span></div>
              <div className="detail-row"><span>Min Speed:</span><span>800 RPM</span></div>
              <div className="detail-row"><span>Max Speed:</span><span>2000 RPM</span></div>
            </div>
          </div>
        );
      case 'help':
        return (
          <div className="bios-help">
            <h3>BIOS HELP</h3>
            <div className="help-item"><span className="key">F1</span> Enter Advanced Mode</div>
            <div className="help-item"><span className="key">F2</span> Add to Favorites</div>
            <div className="help-item"><span className="key">F5</span> Restore Defaults</div>
            <div className="help-item"><span className="key">F7</span> Advanced Mode</div>
            <div className="help-item"><span className="key">F10</span> Save & Exit</div>
            <div className="help-item"><span className="key">F12</span> Boot Menu</div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={`app ${darkMode ? 'dark' : ''}`}>
      <aside className={`sidebar ${darkMode ? 'dark' : ''}`}>
        <div className="sidebar-header">
          <h1>KOVAL_DEV</h1>
          <button
            type="button"
            onClick={() => setDarkMode((value) => !value)}
            className="theme-btn"
            aria-label={darkMode ? 'Включить светлую тему' : 'Включить тёмную тему'}
          >
            {darkMode ? <ImSun size={20} /> : <ImContrast size={20} />}
          </button>
        </div>
        <nav className="nav-menu" aria-label="Главное меню">
          {MENU_ITEMS.map((item) => {
            const IconComponent = item.icon;
            return (
              <button
                type="button"
                key={item.id}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
                aria-current={activeTab === item.id ? 'page' : undefined}
              >
                <IconComponent className="nav-icon" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <main className="main-content">
        {activeTab === 'home' && <HomePage darkMode={darkMode} />}
        {activeTab === 'bios' && (
          <div className={`msi-bios ${darkMode ? 'dark' : ''}`}>
            <div className="bios-top-bar">
              <div className="bios-time">
                <div className="time-value">{time.toLocaleTimeString('ru-RU')}</div>
                <div className="time-date">{time.toLocaleDateString('ru-RU', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })}</div>
              </div>
              <div className="bios-temp">
                <div className="temp-item">
                  <div className="temp-label">CPU Temp</div>
                  <div className="temp-value">{cpuTemp.toFixed(0)}°C</div>
                </div>
                <div className="temp-item">
                  <div className="temp-label">MB Temp</div>
                  <div className="temp-value">{mbTemp.toFixed(0)}°C</div>
                </div>
              </div>
              <div className="bios-info-right">
                <div className="info-row"><span>CPU Speed:</span><span className="highlight">{cpuFreq.toFixed(2)} GHz</span></div>
                <div className="info-row"><span>DDR Speed:</span><span className="highlight">2133 MHz</span></div>
                <div className="info-row"><span>Memory:</span><span>16384MB</span></div>
              </div>
            </div>

            <div className="bios-main">
              <div className="bios-sidebar">
                {BIOS_SECTIONS.map((section) => {
                  const IconComponent = section.icon;
                  return (
                    <button
                      type="button"
                      key={section.id}
                      className={`bios-menu-item ${biosSection === section.id ? 'active' : ''}`}
                      onClick={() => setBiosSection(section.id)}
                    >
                      <IconComponent />
                      <span>{section.label}</span>
                    </button>
                  );
                })}
              </div>

              <div className="bios-content">
                {renderBiosContent()}

                <div className="bios-charts">
                  <div className="chart-item">
                    <div className="chart-label">CPU Load</div>
                    <div className="chart-bar"><div className="chart-fill blue" style={{ width: `${cpuLoad}%` }} /></div>
                    <div className="chart-value">{cpuLoad}%</div>
                  </div>
                  <div className="chart-item">
                    <div className="chart-label">RAM Usage</div>
                    <div className="chart-bar"><div className="chart-fill cyan" style={{ width: `${ramUsage}%` }} /></div>
                    <div className="chart-value">{ramUsage}%</div>
                  </div>
                </div>

                <div className="bios-toggles">
                  <div className="toggle-item">
                    <span>Fast Boot</span>
                    <button
                      type="button"
                      className={`toggle-switch ${fastBoot ? 'on' : ''}`}
                      onClick={() => setFastBoot((value) => !value)}
                      role="switch"
                      aria-checked={fastBoot}
                    ><span className="toggle-circle" /></button>
                  </div>
                  <div className="toggle-item">
                    <span>AHCI Activated</span>
                    <button
                      type="button"
                      className={`toggle-switch ${ahci ? 'on' : ''}`}
                      onClick={() => setAhci((value) => !value)}
                      role="switch"
                      aria-checked={ahci}
                    ><span className="toggle-circle" /></button>
                  </div>
                  <div className="toggle-item">
                    <span>HD Audio</span>
                    <button
                      type="button"
                      className={`toggle-switch ${hdAudio ? 'on' : ''}`}
                      onClick={() => setHdAudio((value) => !value)}
                      role="switch"
                      aria-checked={hdAudio}
                    ><span className="toggle-circle" /></button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        {!['home', 'bios'].includes(activeTab) && (
          <InfoSection sectionId={activeTab} darkMode={darkMode} />
        )}
      </main>
    </div>
  );
}

export default App;