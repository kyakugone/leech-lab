import { useEffect, useState } from "react";

type Sentence = { japanese: string; english: string };
type Passage = {
  id: number;
  words: string;
  data: {
    sentences: Sentence[];
    question: string;
    choices: string[];
    answer: number;
  };
};

function highlight(text: string) {
  const parts = text.split(/\[\[|\]\]/);
  return parts.map((part, i) =>
    i % 2 === 1 ? <span key={i} style={{ color: "crimson" }}>{part}</span> : part
  );
}

function App() {
  const [passages, setPassages] = useState<Passage[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/passages")
      .then((res) => res.json())
      .then(setPassages);
  }, []);

  if (passages.length === 0) return <p>Loading...</p>;

  const passage = passages[0];

  return (
    <main style={{ maxWidth: 700, margin: "2rem auto", fontSize: "1.25rem", lineHeight: 2 }}>
      <p>
        {passage.data.sentences.map((s, i) => (
          <span key={i}>{highlight(s.japanese)}</span>
        ))}
      </p>

      <p>{passage.data.question}</p>
      {passage.data.choices.map((choice, i) => (
        <button key={i} style={{ display: "block", margin: "0.5rem 0" }}>
          {i + 1}. {choice}
        </button>
      ))}
    </main>
  );
}

export default App;