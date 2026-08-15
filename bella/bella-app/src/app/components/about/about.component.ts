import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page-container">
      <h1>👥 Quiénes somos</h1>
      
      <div class="content">
        <div class="card">
          <h2>Nuestra misión</h2>
          <p>
            Democratizar la <strong>inteligencia artificial</strong> mediante sistemas 
            ligeros, accesibles y transparentes. Creemos que la IA no necesita 
            enormes centros de datos para ser útil.
          </p>
        </div>
        
        <div class="card">
          <h2>El equipo</h2>
          <p>
            <strong>Uziel</strong> — Desarrollador principal<br>
            Especialista en sistemas distribuidos y arquitecturas de memoria asociativa.
          </p>
          <p>
            <strong>Bella</strong> — IA experimental<br>
            Entrenada con miles de palabras para aprender patrones lingüísticos.
          </p>
        </div>
        
        <div class="card">
          <h2>Tecnologías</h2>
          <ul>
            <li>⚡ <strong>Angular 19</strong> — Framework frontend</li>
            <li>🔢 <strong>BigInt & Bitwise</strong> — Operaciones de bajo nivel</li>
            <li>🧩 <strong>Arquitectura SPA</strong> — Sin recargas pesadas</li>
            <li>📦 <strong>Node.js</strong> — Backend ligero</li>
          </ul>
        </div>
        
        <div class="card">
          <h2>Filosofía</h2>
          <blockquote>
            "Menos es más. Una interfaz limpia y texto puro es suficiente 
            para comunicarse con una IA."
          </blockquote>
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
      font-size: 2.5em;
      color: #ffaa00;
      border-bottom: 2px solid #ffaa00;
      padding-bottom: 10px;
    }
    .card {
      background: #141414;
      padding: 20px;
      margin: 25px 0;
      border-left: 3px solid #00ff41;
      border-radius: 0 4px 4px 0;
    }
    .card h2 {
      color: #00ff41;
      margin-top: 0;
    }
    .card ul {
      list-style: none;
      padding: 0;
    }
    .card ul li {
      padding: 8px 0;
    }
    blockquote {
      font-style: italic;
      color: #88ff88;
      padding: 15px;
      border: 1px solid #00ff41;
      border-radius: 4px;
      background: #0a0a0a;
    }
  `
})
export class AboutComponent {}
