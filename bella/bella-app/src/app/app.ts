import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule, RouterOutlet],
  template: `
    <nav class="navbar">
      <div class="nav-brand">🐚 Bella</div>
      <div class="nav-links">
        <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Inicio</a>
        <a routerLink="/about" routerLinkActive="active">Quiénes somos</a>
        <a routerLink="/bella" routerLinkActive="active">Bella IA</a>
      </div>
    </nav>
    
    <main>
      <router-outlet></router-outlet>
    </main>
    
    <footer class="footer">
      <p>Bella AI v2.0 — Hecho con ❤️ y texto puro | Sin imágenes, solo código</p>
    </footer>
  `,
  styles: `
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    :host {
      display: block;
      background: #0d0d0d;
      min-height: 100vh;
      font-family: 'Courier New', monospace;
    }
    .navbar {
      background: #0a0a0a;
      padding: 15px 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1a1a1a;
      flex-wrap: wrap;
    }
    .nav-brand {
      color: #00ff41;
      font-size: 1.5em;
      font-weight: bold;
      text-shadow: 0 0 10px rgba(0,255,65,0.2);
    }
    .nav-links {
      display: flex;
      gap: 25px;
    }
    .nav-links a {
      color: #88ff88;
      text-decoration: none;
      padding: 5px 10px;
      transition: all 0.3s;
      border-bottom: 2px solid transparent;
    }
    .nav-links a:hover {
      color: #00ff41;
      border-bottom-color: #00ff41;
    }
    .nav-links a.active {
      color: #00ff41;
      border-bottom-color: #ffaa00;
      font-weight: bold;
    }
    footer {
      text-align: center;
      padding: 20px;
      color: #446644;
      border-top: 1px solid #1a1a1a;
      font-size: 0.9em;
    }
    @media (max-width: 600px) {
      .navbar {
        flex-direction: column;
        gap: 10px;
      }
      .nav-links {
        flex-wrap: wrap;
        justify-content: center;
      }
    }
  `
})
export class App {
  title = 'bella-app';
}
