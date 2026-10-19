'use client' // Note que agora está correto: 'use client'

import { useState, useEffect } from 'react';
import MetricCard from './components/MetricCard';
import LoadingBar from './components/loadingBar';

export default function Dashboard(){
  const [metrics, setMetrics] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/metrics')
    .then((res) => res.json())
    .then((data) => {
      setMetrics(data), setLoading(false)
    })
    .catch((err) => {
      console.error("erro ao solicitar dados a api", err),
      setLoading(false)
    })
  },[]);


  if (loading){
    <LoadingBar/>
  }

  return (
    <main className="min-h-screen bg-mauve-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
      {/* Cabeçalho da dashboard*/}
      <header className="mb-8">
        <h1 className='text-3xl font-extrabold text-emerald-400'>Dashboard</h1>
        <p className='text-slate-400 lowercase'>Your Business in Your Hands</p>
      </header>

      {/*Grid de Cards*/}
      <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
        <MetricCard
          title='Lucro Diário'
          data= {metrics?.data?.profit_days}
          titleColor='text-emerald-400'
        />

        <MetricCard
        title='Lucro Por Categoria'
        data={metrics?.data?.profit_categories}
        titleColor='text-emerald-400'
        />  
        
      </div>
      

    </main>
  )
  

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