(() => {
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  };

  const postForm = async (url, data) => {
    const body = new URLSearchParams(data);
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      },
      body,
      credentials: 'same-origin',
    });
    const json = await response.json().catch(() => ({ ok: false, error: 'ошибка ответа сервера' }));
    return { response, json };
  };

  const handleVote = async (btn) => {
    const targetType = btn.dataset.targetType;
    const targetId = btn.dataset.targetId;
    const voteType = btn.dataset.voteType;
    const url = targetType === 'question' ? '/api/question/vote/' : '/api/answer/vote/';
    const { response, json } = await postForm(url, { target_id: targetId, vote_type: voteType });
    if (!response.ok || !json.ok) {
      if (response.status === 403 && json.login_url) {
        window.location.href = json.login_url;
        return;
      }
      if (response.status === 403) {
        alert('ошибка csrf или доступ запрещен');
        return;
      }
      if (response.status === 405) {
        alert('неверный метод запроса');
        return;
      }
      alert(json.error || 'не удалось проголосовать');
      return;
    }
    document.querySelectorAll(`.js-rating[data-target-type="${targetType}"][data-target-id="${json.target_id}"]`)
      .forEach((el) => {
        el.textContent = String(json.rating);
      });
    document.querySelectorAll(`.js-vote-btn[data-target-type="${targetType}"][data-target-id="${json.target_id}"]`)
      .forEach((el) => {
        el.disabled = true;
        el.title = 'вы уже голосовали';
      });
  };

  const handleCorrect = async (btn) => {
    const questionId = btn.dataset.questionId;
    const answerId = btn.dataset.answerId;
    const { response, json } = await postForm('/api/answer/correct/', { question_id: questionId, answer_id: answerId });
    if (!response.ok || !json.ok) {
      if (response.status === 403 && json.login_url) {
        window.location.href = json.login_url;
        return;
      }
      if (response.status === 403) {
        alert('ошибка csrf или доступ запрещен');
        return;
      }
      if (response.status === 405) {
        alert('неверный метод запроса');
        return;
      }
      alert(json.error || 'не удалось отметить ответ');
      return;
    }
    document.querySelectorAll('.js-correct-label').forEach((el) => {
      const isSelected = Number(el.dataset.answerId) === Number(json.answer_id);
      el.textContent = isSelected ? 'Правильный ответ' : 'Обычный ответ';
      el.classList.toggle('text-success', isSelected);
      el.classList.toggle('text-muted', !isSelected);
    });
    document.querySelectorAll('.js-answer-card').forEach((card) => {
      const isSelected = Number(card.dataset.answerId) === Number(json.answer_id);
      card.classList.toggle('border-success', isSelected);
      card.classList.toggle('border-secondary', !isSelected);
    });
  };

  document.addEventListener('click', (event) => {
    const voteBtn = event.target.closest('.js-vote-btn');
    if (voteBtn) {
      event.preventDefault();
      handleVote(voteBtn);
      return;
    }
    const correctBtn = event.target.closest('.js-correct-btn');
    if (correctBtn) {
      event.preventDefault();
      handleCorrect(correctBtn);
    }
  });

  const initSearchSuggestions = () => {
    const input = document.querySelector('.js-search-input');
    const list = document.querySelector('.js-search-suggestions');
    if (!input || !list) {
      return;
    }
    const url = input.dataset.suggestionsUrl;
    let timer = null;
    let requestId = 0;

    const hideSuggestions = () => {
      list.hidden = true;
      list.innerHTML = '';
    };

    const showSuggestions = (items) => {
      list.innerHTML = '';
      if (!items.length) {
        hideSuggestions();
        return;
      }
      items.forEach((item) => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        link.className = 'search-suggestions__item';
        li.appendChild(link);
        list.appendChild(li);
      });
      list.hidden = false;
    };

    const fetchSuggestions = async (query) => {
      const currentId = ++requestId;
      const response = await fetch(`${url}?q=${encodeURIComponent(query)}`, { credentials: 'same-origin' });
      const json = await response.json().catch(() => ({ results: [] }));
      if (currentId !== requestId) {
        return;
      }
      showSuggestions(json.results || []);
    };

    input.addEventListener('input', () => {
      clearTimeout(timer);
      const query = input.value.trim();
      if (query.length < 2) {
        requestId += 1;
        hideSuggestions();
        return;
      }
      timer = setTimeout(() => {
        fetchSuggestions(query);
      }, 350);
    });

    input.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        hideSuggestions();
      }
    });

    document.addEventListener('click', (event) => {
      if (!event.target.closest('.search-form-wrapper')) {
        hideSuggestions();
      }
    });
  };

  initSearchSuggestions();
})();
