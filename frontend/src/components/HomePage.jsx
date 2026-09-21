import { useEffect, useRef, useState } from 'react';

import { SURVEY_QUESTIONS } from '../data/questions';
import { submitSurvey } from '../services/surveyApi';

const INTRO_DELAY_MS = 1600;
const QUESTION_TRANSITION_MS = 320;

function HomePage({ darkMode }) {
  const [phoneState, setPhoneState] = useState('loading');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [animationDirection, setAnimationDirection] = useState('');
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [userPhone, setUserPhone] = useState('');
  const [website, setWebsite] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const introTimerRef = useRef(null);
  const transitionTimerRef = useRef(null);
  const enterTimerRef = useRef(null);
  const phoneRef = useRef(null);

  const clearTimers = () => {
    window.clearTimeout(introTimerRef.current);
    window.clearTimeout(transitionTimerRef.current);
    window.clearTimeout(enterTimerRef.current);
  };

  useEffect(() => {
    introTimerRef.current = window.setTimeout(() => setPhoneState('question'), INTRO_DELAY_MS);
    return clearTimers;
  }, []);

  const handleAnswer = (answer) => {
    if (isTransitioning) return;

    const question = SURVEY_QUESTIONS[currentQuestion];
    setIsTransitioning(true);
    setAnimationDirection('exit');

    transitionTimerRef.current = window.setTimeout(() => {
      setAnswers((previousAnswers) => [
        ...previousAnswers,
        { question: question.text, answer },
      ]);

      if (currentQuestion < SURVEY_QUESTIONS.length - 1) {
        setCurrentQuestion((previousQuestion) => previousQuestion + 1);
        setAnimationDirection('enter');
        enterTimerRef.current = window.setTimeout(() => {
          setAnimationDirection('');
          setIsTransitioning(false);
        }, 80);
      } else {
        setAnimationDirection('');
        setIsTransitioning(false);
        setPhoneState('contact');
      }
    }, QUESTION_TRANSITION_MS);
  };

  const handleSubmitSurvey = async (event) => {
    event.preventDefault();
    if (isSubmitting) return;

    if (answers.length !== SURVEY_QUESTIONS.length) {
      setSubmitError('Опрос заполнен не полностью. Пройдите его ещё раз.');
      return;
    }

    setSubmitError('');
    setIsSubmitting(true);

    try {
      await submitSurvey({
        answers,
        user_email: userEmail.trim(),
        user_phone: userPhone.trim(),
        website,
      });
      setPhoneState('result');
    } catch (error) {
      console.error('Ошибка отправки опроса:', error);
      setSubmitError(error.message || 'Не удалось отправить заявку.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRestart = () => {
    clearTimers();
    setPhoneState('loading');
    setAnswers([]);
    setCurrentQuestion(0);
    setAnimationDirection('');
    setIsTransitioning(false);
    setUserEmail('');
    setUserPhone('');
    setWebsite('');
    setSubmitError('');
    introTimerRef.current = window.setTimeout(() => setPhoneState('question'), INTRO_DELAY_MS);
  };

  const focusSurvey = () => {
    phoneRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  return (
    <div className={`home-page ${darkMode ? 'dark' : ''}`}>
      <div className="home-content">
        <section className="home-left" aria-labelledby="home-title">
          <h1 id="home-title" className="home-title">Создаем сайты под ключ</h1>
          <p className="home-subtitle">От идеи до запуска за 2 недели</p>

          <div className="home-features">
            <div className="feature-item">
              <span className="feature-icon" aria-hidden="true">⚡</span>
              <div><h3>Быстрая разработка</h3><p>Используем современные технологии для быстрого запуска вашего проекта</p></div>
            </div>
            <div className="feature-item">
              <span className="feature-icon" aria-hidden="true">✦</span>
              <div><h3>Уникальный дизайн</h3><p>Каждый проект создается с нуля под ваши задачи и бренд</p></div>
            </div>
            <div className="feature-item">
              <span className="feature-icon" aria-hidden="true">∞</span>
              <div><h3>Полная поддержка</h3><p>Техническое обслуживание и обновление после запуска</p></div>
            </div>
          </div>

          <div className="home-stats">
            <div className="stat-item"><div className="stat-number">50+</div><div className="stat-text">Проектов</div></div>
            <div className="stat-item"><div className="stat-number">98%</div><div className="stat-text">Довольных клиентов</div></div>
            <div className="stat-item"><div className="stat-number">24/7</div><div className="stat-text">Поддержка</div></div>
          </div>
          <button type="button" className="cta-button" onClick={focusSurvey}>Обсудить проект</button>
        </section>

        <div className="home-right" ref={phoneRef}>
          <div className="phone-container">
            <div className="phone-frame">
              <div className="phone-screen" aria-live="polite">
                {phoneState === 'loading' && (
                  <div className="phone-loading">
                    <div className="loading-logo" aria-hidden="true">📱</div>
                    <div className="loading-text">Quick Test</div>
                    <div className="loading-bar"><div className="loading-progress" /></div>
                    <div className="loading-dots" aria-label="Загрузка"><span /><span /><span /></div>
                  </div>
                )}

                {phoneState === 'question' && (
                  <div className={`question-container ${animationDirection}`}>
                    <div className="phone-header">
                      <span>Вопрос {currentQuestion + 1} из {SURVEY_QUESTIONS.length}</span>
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{ width: `${((currentQuestion + 1) / SURVEY_QUESTIONS.length) * 100}%` }}
                        />
                      </div>
                    </div>
                    <div className="phone-content">
                      <div className="question-block">
                        <p className="question-text">{SURVEY_QUESTIONS[currentQuestion].text}</p>
                        <div className="options-list">
                          {SURVEY_QUESTIONS[currentQuestion].options.map((option) => (
                            <button
                              key={option}
                              type="button"
                              className="option-btn"
                              onClick={() => handleAnswer(option)}
                              disabled={isTransitioning}
                            >
                              {option}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {phoneState === 'contact' && (
                  <div className="contact-container">
                    <div className="phone-header"><span>Последний шаг</span></div>
                    <div className="phone-content contact-content">
                      <form className="contact-form" onSubmit={handleSubmitSurvey}>
                        <p className="contact-title">Куда отправить предложение?</p>
                        <label className="input-label" htmlFor="survey-email">Email</label>
                        <input
                          id="survey-email"
                          type="email"
                          className="contact-input"
                          placeholder="name@example.com"
                          value={userEmail}
                          onChange={(event) => setUserEmail(event.target.value)}
                          autoComplete="email"
                          maxLength={254}
                          disabled={isSubmitting}
                          required
                        />
                        <label className="input-label" htmlFor="survey-phone">Телефон</label>
                        <input
                          id="survey-phone"
                          type="tel"
                          className="contact-input"
                          placeholder="+7 999 123-45-67"
                          value={userPhone}
                          onChange={(event) => setUserPhone(event.target.value)}
                          autoComplete="tel"
                          pattern="[0-9+() .-]{7,40}"
                          maxLength={40}
                          disabled={isSubmitting}
                          required
                        />
                        <div className="honeypot" aria-hidden="true">
                          <label htmlFor="survey-website">Ваш сайт</label>
                          <input
                            id="survey-website"
                            type="text"
                            value={website}
                            onChange={(event) => setWebsite(event.target.value)}
                            tabIndex={-1}
                            autoComplete="off"
                          />
                        </div>
                        {submitError && <div className="contact-error" role="alert">{submitError}</div>}
                        <button className="submit-btn" type="submit" disabled={isSubmitting}>
                          {isSubmitting ? (
                            <span className="submit-status"><span className="submit-spinner" aria-hidden="true" />Отправляем...</span>
                          ) : 'Отправить результаты'}
                        </button>
                        {isSubmitting && <p className="contact-hint">Проверяем доставку письма. Ожидание ограничено 20 секундами.</p>}
                      </form>
                    </div>
                  </div>
                )}

                {phoneState === 'result' && (
                  <div className="result-container">
                    <div className="phone-header"><span>Готово!</span></div>
                    <div className="phone-content">
                      <div className="result-block">
                        <div className="result-icon" aria-hidden="true">✓</div>
                        <h3>Спасибо за ответы!</h3>
                        <p>Заявка и результаты опроса отправлены. Мы свяжемся с вами по адресу {userEmail}.</p>
                        <div className="result-stats">
                          <div className="result-stat"><div className="result-number">{answers.length}</div><div className="result-label">Вопросов</div></div>
                          <div className="result-stat"><div className="result-number">24ч</div><div className="result-label">На связь</div></div>
                        </div>
                        <button type="button" className="restart-btn" onClick={handleRestart}>Пройти ещё раз</button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
