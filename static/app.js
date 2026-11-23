const $ = (id) => document.getElementById(id);
let tickets = [];

async function api(path, options = {}) {
  const response = await fetch(path, {headers: {'Content-Type': 'application/json'}, ...options});
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || 'Something went wrong.');
  }
  return response.status === 204 ? null : response.json();
}

function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function render() {
  $('total').textContent = tickets.length;
  $('open').textContent = tickets.filter(t => t.status === 'Open').length;
  $('progress').textContent = tickets.filter(t => t.status === 'In Progress').length;
  $('resolved').textContent = tickets.filter(t => t.status === 'Resolved').length;
  const visible = tickets.filter(t => $('filter').value === 'All' || t.status === $('filter').value);
  const list = $('tickets');
  list.replaceChildren();
  if (!visible.length) {
    list.append(el('div', 'No tickets found. Create one to get started!', 'empty'));
    return;
  }
  for (const ticket of visible) {
    const card = el('article', undefined, 'ticket');
    const head = el('div', undefined, 'ticket-head');
    head.append(el('h3', `#${ticket.id}  ${ticket.title}`), el('span', ticket.priority, `pill ${ticket.priority}`));
    const description = el('p', ticket.description || 'No description provided.');
    const meta = el('div', undefined, 'ticket-meta');
    const date = el('small', `Created: ${ticket.created_at} UTC`);
    const actions = el('div', undefined, 'actions');
    const status = el('select');
    status.setAttribute('aria-label', `Status for ticket ${ticket.id}`);
    for (const option of ['Open', 'In Progress', 'Resolved']) {
      const item = el('option', option);
      item.value = option;
      status.append(item);
    }
    status.value = ticket.status;
    status.addEventListener('change', async () => {
      try {
        await api(`/api/tickets/${ticket.id}`, {method: 'PATCH', body: JSON.stringify({status: status.value})});
        await load();
      } catch (error) { $('message').textContent = error.message; status.value = ticket.status; }
    });
    const remove = el('button', 'Delete', 'delete');
    remove.type = 'button';
    remove.setAttribute('aria-label', `Delete ticket ${ticket.id}`);
    remove.addEventListener('click', async () => {
      if (!confirm(`Delete ticket #${ticket.id}?`)) return;
      try { await api(`/api/tickets/${ticket.id}`, {method: 'DELETE'}); await load(); }
      catch (error) { $('message').textContent = error.message; }
    });
    actions.append(status, remove);
    meta.append(date, actions);
    card.append(head, description, meta);
    list.append(card);
  }
}

async function load() {
  try { tickets = await api('/api/tickets'); $('message').textContent = ''; render(); }
  catch (error) { $('message').textContent = error.message; }
}

$('ticket-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector('button[type=submit]');
  button.disabled = true;
  try {
    await api('/api/tickets', {method: 'POST', body: JSON.stringify({
      title: $('title').value, description: $('description').value, priority: $('priority').value
    })});
    form.reset();
    await load();
  } catch (error) { $('message').textContent = error.message; }
  finally { button.disabled = false; }
});
$('filter').addEventListener('change', render);
load();
