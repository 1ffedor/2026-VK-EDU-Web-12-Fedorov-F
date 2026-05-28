(() => {
  const config = window.questionRealtimeConfig;
  if (!config || typeof Centrifuge === 'undefined') {
    return;
  }

  const answersList = document.getElementById('answers-list');
  if (!answersList) {
    return;
  }

  const answersTitle = answersList.querySelector('.js-answers-title');
  const answersItems = answersList.querySelector('.js-answers-items');
  const answersEmpty = answersList.querySelector('.js-answers-empty');

  const answersNoun = (count) => {
    const n = Math.abs(Number(count)) % 100;
    if (n >= 11 && n <= 14) return 'ответов';
    const m = n % 10;
    if (m === 1) return 'ответ';
    if (m >= 2 && m <= 4) return 'ответа';
    return 'ответов';
  };

  const updateAnswersTitle = (count) => {
    if (answersTitle) {
      answersTitle.textContent = `${count} ${answersNoun(count)}`;
    }
  };

  const fetchAnswerCard = async (answerId) => {
    const url = config.cardUrlTemplate.replace('/0/', `/${answerId}/`);
    const response = await fetch(url, { credentials: 'same-origin' });
    const json = await response.json();
    if (!response.ok || !json.ok) {
      throw new Error('не удалось загрузить ответ');
    }
    return json.html;
  };

  const appendAnswer = async (answerId) => {
    const html = await fetchAnswerCard(answerId);
    if (answersEmpty) {
      answersEmpty.remove();
    }
    const wrapper = document.createElement('div');
    wrapper.innerHTML = html.trim();
    const card = wrapper.firstElementChild;
    if (!card) {
      return;
    }
    answersItems.appendChild(card);
    const count = Number(answersList.dataset.answersCount || 0) + 1;
    answersList.dataset.answersCount = String(count);
    updateAnswersTitle(count);
  };

  const handleNewAnswer = async (answerId) => {
    const currentPage = Number(config.currentPage || 1);
    if (currentPage !== 1) {
      alert('Появился новый ответ к этому вопросу');
      return;
    }
    if (document.querySelector(`.js-answer-card[data-answer-id="${answerId}"]`)) {
      return;
    }
    try {
      await appendAnswer(answerId);
    } catch (error) {
      alert('Появился новый ответ, но не удалось обновить список');
    }
  };

  const connect = async () => {
    const tokenResponse = await fetch(config.tokenUrl, { credentials: 'same-origin' });
    const tokenJson = await tokenResponse.json();
    const centrifuge = new Centrifuge(config.wsUrl, { token: tokenJson.token });
    const subscription = centrifuge.newSubscription(config.channel);
    subscription.on('publication', (ctx) => {
      const data = ctx.data || {};
      if (data.type === 'new_answer' && Number(data.question_id) === Number(config.questionId)) {
        handleNewAnswer(Number(data.answer_id));
      }
    });
    subscription.subscribe();
    centrifuge.connect();
  };

  connect().catch(() => {});
})();
