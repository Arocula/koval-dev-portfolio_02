const API_BASE_URL = (import.meta.env.VITE_API_URL || '').trim().replace(/\/$/, '');
const DEFAULT_TIMEOUT_MS = 20000;

export class SurveyApiError extends Error {
  constructor(message, { code = 'survey_error', status = 0, submissionId = null } = {}) {
    super(message);
    this.name = 'SurveyApiError';
    this.code = code;
    this.status = status;
    this.submissionId = submissionId;
  }
}

function extractError(responseBody, status) {
  const detail = responseBody?.detail;
  if (detail && typeof detail === 'object' && !Array.isArray(detail)) {
    return new SurveyApiError(detail.message || 'Не удалось отправить заявку.', {
      code: detail.code,
      status,
      submissionId: detail.submission_id,
    });
  }

  if (typeof detail === 'string') {
    return new SurveyApiError(detail, { status });
  }

  if (status === 422) {
    return new SurveyApiError('Проверьте корректность email и телефона.', {
      code: 'validation_error',
      status,
    });
  }

  return new SurveyApiError('Сервер не смог отправить заявку. Попробуйте ещё раз.', { status });
}

export async function submitSurvey(payload, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${API_BASE_URL}/api/survey`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    let body = null;
    try {
      body = await response.json();
    } catch {
      body = null;
    }

    if (!response.ok) {
      throw extractError(body, response.status);
    }

    return body;
  } catch (error) {
    if (error?.name === 'AbortError') {
      throw new SurveyApiError(
        'Почтовый сервер не ответил вовремя. Загрузка остановлена — проверьте backend и повторите отправку.',
        { code: 'request_timeout' },
      );
    }

    if (error instanceof SurveyApiError) {
      throw error;
    }

    throw new SurveyApiError(
      'Нет соединения с backend. Убедитесь, что окно FastAPI запущено на порту 8000.',
      { code: 'network_error' },
    );
  } finally {
    window.clearTimeout(timeoutId);
  }
}
