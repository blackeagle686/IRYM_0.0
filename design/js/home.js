/* File: script.js */
document.getElementById('promptForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const prompt = document.getElementById('userPrompt').value;

  // Simulate suggestion flow
  const suggestions = [
    'Add a sunset in the background?',
    'Should the character be realistic or cartoon style?',
    'Include some animals or buildings?'
  ];

  const suggestionList = document.getElementById('suggestionList');
  suggestionList.innerHTML = '';
  suggestions.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    suggestionList.appendChild(li);
  });
  document.getElementById('suggestions').classList.remove('hidden');
  document.getElementById('result').style.display = 'block';
  // Fake generated image preview (use real backend later)
  document.getElementById('generatedImage').src = 'https://via.placeholder.com/600x400.png?text=Generated+Image';
});

// Sidebar toggle logic
document.getElementById('toggleSidebar').addEventListener('click', () => {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('hidden');
});
