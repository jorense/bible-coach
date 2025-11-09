const chatContainer = document.querySelector('#chat');
const form = document.querySelector('#chat-form');
const textarea = document.querySelector('#message');

const conversation = [];

const templates = {
  user: (content) => `
    <article class="message message--user">
      <div class="message__avatar" aria-hidden="true">🙋‍♀️</div>
      <div class="message__content">${content}</div>
    </article>
  `,
  assistant: (content) => `
    <article class="message message--assistant">
      <div class="message__avatar" aria-hidden="true">🤖</div>
      <div class="message__content">${content}</div>
    </article>
  `,
};

function addMessage(role, content) {
  conversation.push({ role, content });
  chatContainer.insertAdjacentHTML('beforeend', templates[role](escapeHtml(content)));
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

async function sendMessage(event) {
  event.preventDefault();
  const message = textarea.value.trim();
  if (!message) return;

  textarea.value = '';
  addMessage('user', message);
  setFormDisabled(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages: conversation }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    addMessage('assistant', data.reply);
  } catch (error) {
    addMessage('assistant', 'Sorry, something went wrong. Please try again.');
    console.error(error);
  } finally {
    setFormDisabled(false);
    textarea.focus();
  }
}

function setFormDisabled(state) {
  textarea.disabled = state;
  form.querySelector('button').disabled = state;
}

form.addEventListener('submit', sendMessage);

// greet on load
addMessage(
  'assistant',
  "Hello! I'm your Bible Coach. Let's walk through Observation, Interpretation, and Application together. Share the passage you're studying so we can begin."
);
