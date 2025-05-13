// ===== DONNÉES DU QUIZ =====
const quizData = [
  {
    question: "Si une équipe marque 2 buts en première mi-temps et 3 en seconde, quel est le score final ?",
    options: ["2-3", "3-2", "5-0"],
    answer: 2,
    explanation: "2 + 3 = 5 buts au total"
  },
  {
    question: "Quel pays a inventé le football moderne ?",
    options: ["Brésil", "France", "Angleterre"],
    answer: 2,
    explanation: "Les règles modernes ont été codifiées en Angleterre en 1863"
  },
  {
    question: "Combien de joueurs composent une équipe de football ?",
    options: ["9", "11", "13"],
    answer: 1,
    explanation: "11 joueurs dont 1 gardien"
  }
];

let currentQuestion = 0;
let score = 0;

// ===== FONCTIONS =====
function loadQuestion() {
  if (currentQuestion >= quizData.length) {
    showResults();
    return;
  }

  const q = quizData[currentQuestion];
  document.getElementById('question').innerHTML = q.question;
  document.getElementById('progress').textContent = `Question ${currentQuestion + 1}/${quizData.length}`;
  
  let optionsHtml = '';
  q.options.forEach((option, index) => {
    optionsHtml += `
      <button onclick="checkAnswer(${index})" 
        class="p-4 bg-white/10 rounded-lg hover:bg-yellow-500/20 transition">
        ${String.fromCharCode(65 + index)}. ${option}
      </button>
    `;
  });
  
  document.getElementById('options').innerHTML = optionsHtml;
  document.getElementById('next-btn').classList.add('hidden');
  document.getElementById('result').classList.add('hidden');
}

function checkAnswer(selectedIndex) {
  const q = quizData[currentQuestion];
  const options = document.querySelectorAll('#options button');
  
  // Désactive tous les boutons
  options.forEach(btn => btn.disabled = true);
  
  // Met en évidence la réponse
  options.forEach((btn, index) => {
    if (index === q.answer) {
      btn.classList.add('bg-green-500/30', 'border-green-500');
    } else if (index === selectedIndex) {
      btn.classList.add('bg-red-500/30', 'border-red-500');
    }
  });

  // Affiche l'explication
  document.getElementById('explanation').innerHTML = `💡 ${q.explanation}`;
  document.getElementById('result').classList.remove('hidden');
  
  // Met à jour le score
  if (selectedIndex === q.answer) {
    score++;
    document.getElementById('score').innerHTML = `✅ Score : ${score}/${quizData.length}`;
  } else {
    document.getElementById('score').innerHTML = `❌ Score : ${score}/${quizData.length}`;
  }
  
  document.getElementById('next-btn').classList.remove('hidden');
}

function showResults() {
  document.getElementById('quiz-container').innerHTML = `
    <div class="text-center">
      <h2 class="text-3xl font-bold mb-6">Quiz Terminé !</h2>
      <p class="text-2xl mb-8">Ton score : ${score}/${quizData.length}</p>
      <button onclick="location.reload()" class="px-6 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg font-bold">
        Rejouer
      </button>
    </div>
  `;
}

// ===== INITIALISATION =====
document.getElementById('next-btn').addEventListener('click', () => {
  currentQuestion++;
  loadQuestion();
});

// Lance le quiz au chargement
if (document.getElementById('quiz-container')) {
  loadQuestion();
}