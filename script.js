/**
 * Application State & Data Management
 */
const STORAGE_KEY = 'journal_entries_data';
let entries = [];
let activeEntryId = null;
let autoSaveTimer = null;

// DOM Elements Cache
const entryListEl = document.getElementById('entryList');
const searchInput = document.getElementById('searchInput');
const newEntryBtn = document.getElementById('newEntryBtn');
const placeholderMsg = document.getElementById('placeholderMsg');
const editorEl = document.getElementById('editor');
const titleInput = document.getElementById('titleInput');
const bodyInput = document.getElementById('bodyInput');
const dateLabel = document.getElementById('dateLabel');
const saveStatus = document.getElementById('saveStatus');
const deleteBtn = document.getElementById('deleteBtn');

/**
 * Helper Utilities
 */
const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  });
};

/**
 * LocalStorage Controller
 */
function loadEntries() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    entries = data ? JSON.parse(data) : [];
  } catch (err) {
    console.error('Failed to parse entries from storage:', err);
    entries = [];
  }
  // Sort entries by last updated date (newest first)
  entries.sort((a, b) => b.updatedAt - a.updatedAt);
  renderList();
}

function saveEntriesToStorage() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  } catch (err) {
    console.error('Failed to save to storage:', err);
    saveStatus.textContent = 'Error saving!';
  }
}

/**
 * UI Rendering Functions
 */
function renderList() {
  const query = searchInput.value.trim().toLowerCase();
  const filteredEntries = entries.filter(e => 
    e.title.toLowerCase().includes(query) || e.body.toLowerCase().includes(query)
  );

  entryListEl.innerHTML = '';

  if (filteredEntries.length === 0) {
    entryListEl.innerHTML = `<div class="placeholder-msg">${entries.length === 0 ? 'No entries yet.' : 'No matches found.'}</div>`;
    return;
  }

  filteredEntries.forEach(entry => {
    const item = document.createElement('div');
    item.className = `entry-item ${entry.id === activeEntryId ? 'active' : ''}`;
    
    item.innerHTML = `
      <div class="date">${formatDate(entry.updatedAt)}</div>
      <div class="title">${entry.title || 'Untitled'}</div>
      <div class="preview">${entry.body || 'No content...'}</div>
    `;
    
    item.addEventListener('click', () => openEntry(entry.id));
    entryListEl.appendChild(item);
  });
}

function openEntry(id) {
  activeEntryId = id;
  const entry = entries.find(e => e.id === id);
  if (!entry) return;

  placeholderMsg.style.display = 'none';
  editorEl.style.display = 'flex';

  dateLabel.textContent = `Last updated: ${formatDate(entry.updatedAt)}`;
  titleInput.value = entry.title;
  bodyInput.value = entry.body;
  saveStatus.textContent = '';

  renderList();
}

/**
 * CRUD Action Handlers
 */
function createEntry() {
  const now = Date.now();
  const newEntry = {
    id: now.toString(),
    title: '',
    body: '',
    updatedAt: now
  };

  entries.unshift(newEntry);
  saveEntriesToStorage();
  openEntry(newEntry.id);
  titleInput.focus();
}

function scheduleAutoSave() {
  saveStatus.textContent = 'Saving...';
  clearTimeout(autoSaveTimer);

  autoSaveTimer = setTimeout(() => {
    const entry = entries.find(e => e.id === activeEntryId);
    if (!entry) return;

    entry.title = titleInput.value;
    entry.body = bodyInput.value;
    entry.updatedAt = Date.now();

    // Maintain sorted order by recency
    entries.sort((a, b) => b.updatedAt - a.updatedAt);
    saveEntriesToStorage();

    dateLabel.textContent = `Last updated: ${formatDate(entry.updatedAt)}`;
    saveStatus.textContent = 'Saved';
    renderList();
  }, 400);
}

function deleteEntry() {
  if (!activeEntryId) return;
  if (!confirm('Are you sure you want to delete this entry?')) return;

  entries = entries.filter(e => e.id !== activeEntryId);
  activeEntryId = null;
  
  saveEntriesToStorage();
  editorEl.style.display = 'none';
  placeholderMsg.style.display = 'block';
  renderList();
}

/**
 * Event Listener Initializations
 */
newEntryBtn.addEventListener('click', createEntry);
deleteBtn.addEventListener('click', deleteEntry);
titleInput.addEventListener('input', scheduleAutoSave);
bodyInput.addEventListener('input', scheduleAutoSave);
searchInput.addEventListener('input', renderList);

// Initialize Application
loadEntries();