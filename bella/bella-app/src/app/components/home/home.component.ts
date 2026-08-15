import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page-container">
      <h1>🐚 Bella AI</h1>
      <p class="subtitle">Sistema de conciencia distribuida basado en redes neuronales experimentales</p>
      
      <div class="content">
        <h2>¿Qué es Bella?</h2>
        <p>
          Bella es un sistema de <strong>procesamiento de lenguaje natural</strong> que utiliza 
          un enfoque híbrido entre <strong>memoria asociativa</strong> y <strong>dinámica de nodos</strong> 
          para generar respuestas contextuales.
        </p>
        
        <h2>Características principales</h2>
        <ul>
          <li>🧠 <strong>Memoria persistente:</strong> Cada palabra entrenada genera un nodo en la red</li>
          <li>⚡ <strong>Procesamiento en tiempo real:</strong> Respuestas inmediatas sin latencia</li>
          <li>🔮 <strong>Proyección semántica:</strong> Genera respuestas basadas en patrones aprendidos</li>
          <li>📊 <strong>Sin imágenes:</strong> Interfaz 100% basada en texto para máxima velocidad</li>
        </ul>
        
        <div class="cta">
          <a routerLink="/bella" class="btn">▶ Probar Bella ahora</a>
        </div>
      </div>
    </div>
  `,
  styles: `
    .page-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 40px 20px;
      color: #00ff41;
      background: #0d0d0d;
      min-height: 80vh;
    }
    h1 {
      font-size: 3em;
      margin-bottom: 0.2em;
      color: #00ff41;
      text-shadow: 0 0 10px rgba(0,255,65,0.3);
    }
    .subtitle {
      color: #00cc33;
      font-size: 1.2em;
      border-left: 3px solid #00ff41;
      padding-left: 15px;
      margin-bottom: 30px;
    }
    h2 {
      color: #ffaa00;
      margin-top: 30px;
      font-size: 1.5em;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    ul li {
      padding: 10px 0;
      border-bottom: 1px solid #1a1a1a;
    }
    ul li strong {
      color: #ffaa00;
    }
    .cta {
      margin-top: 40px;
      text-align: center;
    }
    .btn {
      display: inline-block;
      background: #00ff41;
      color: #0d0d0d;
      padding: 12px 30px;
      text-decoration: none;
      font-weight: bold;
      border-radius: 4px;
      transition: all 0.3s;
    }
    .btn:hover {
      background: #00cc33;
      transform: scale(1.05);
      box-shadow: 0 0 20px rgba(0,255,65,0.3);
    }
  `
})
export class HomeComponent {}
