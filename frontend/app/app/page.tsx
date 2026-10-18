'use client' // Note que agora está correto: 'use client'

import { useState, useEffect } from 'react';

export default function Dashboard(){
  const [metrics, setMetrics] = useState('')
  const [loading, setloading] = useState(true)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/metrics')
    .then((res) => res.json())
    .then((data) => {
      setMetrics(data), setloading(false)
    })
    .catch((err) => console.error("erro ao solicitar dados a api", err))
  },[])

}



// export function Home() {
//   const [mensagem, setMensagem] = useState('');

//   // Quando a página carregar, busca dados do Python
//   useEffect(() => {
//     fetch('http://127.0.0.1:8000/') // Sua rota raiz do FastAPI
//       .then((res) => res.json())
//       .then((data) => setMensagem(JSON.stringify(data)))
//       .catch((err) => console.error("Erro ao conectar com o Python:", err));
//   }, []);

//   return (
//     <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-slate-900 text-white">
//       <div className="bg-slate-800 p-8 rounded-xl shadow-lg border border-slate-700 max-w-md w-full text-center">
//         <h1 className="text-2xl font-bold mb-4 text-emerald-400">Meu Mini Web App 🚀</h1>
//         <p className="text-slate-300 mb-6">Resposta do Backend Python:</p>
//         <div className="bg-slate-950 p-4 rounded text-emerald-300 font-mono text-sm overflow-x-auto">
//           {mensagem || "Carregando dados do Python..."}
//         </div>
//       </div>
//     </main>
//   );
// }