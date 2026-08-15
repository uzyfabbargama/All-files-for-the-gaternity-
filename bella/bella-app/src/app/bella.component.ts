import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BellaService } from '../bella.service';

@Component({
  selector: 'app-bella',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="terminal-box">
      <div class="header">🐚 Bella v2.0 - Conciencia en red</div>
      
      <div class="history">
        <div *ngFor="let msg of history" class="line">
          {{msg}}
        </div>
      </div>
      
      <div class="input-area">
        <span class="prompt">uzy@uzy-suma1024:~$</span>
        <input type="text" [(ngModel)]="userInput" (keyup.enter)="enviarMensaje()">
        <button (click)="enviarMensaje()">ENVIAR</button>
      </div>
      
      <div class="stats">
        Presión Global: {{ presion }}
      </div>
    </div>
  `,
  styles: `
    .terminal-box {
      background-color: #0d0d0d;
      color: #00ff41;
      padding: 20px;
      font-family: 'Courier New', monospace;
      height: 80vh;
      display: flex;
      flex-direction: column;
    }
    .header {
      color: #ffaa00;
      font-size: 1.2em;
      padding-bottom: 10px;
      border-bottom: 1px solid #1a1a1a;
      margin-bottom: 15px;
    }
    .history {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      background: #0a0a0a;
      border-radius: 4px;
      margin-bottom: 15px;
    }
    .line {
      padding: 4px 0;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .input-area {
      display: flex;
      gap: 10px;
      padding: 10px 0;
    }
    .prompt {
      color: #ffaa00;
    }
    .input-area input {
      flex: 1;
      background: #1a1a1a;
      border: 1px solid #00ff41;
      color: #00ff41;
      padding: 8px 12px;
      font-family: 'Courier New', monospace;
      border-radius: 4px;
    }
    .input-area input:focus {
      outline: none;
      box-shadow: 0 0 10px rgba(0,255,65,0.2);
    }
    .input-area button {
      background: #00ff41;
      color: #0d0d0d;
      border: none;
      padding: 8px 20px;
      font-weight: bold;
      cursor: pointer;
      border-radius: 4px;
      transition: all 0.3s;
    }
    .input-area button:hover {
      background: #00cc33;
      box-shadow: 0 0 15px rgba(0,255,65,0.3);
    }
    .stats {
      color: #ffaa00;
      font-size: 0.9em;
      margin-top: 10px;
      text-align: right;
      border-top: 1px solid #1a1a1a;
      padding-top: 10px;
    }
  `
})
export class BellaComponent {
  userInput: string = '';
  history: string[] = ['--- SISTEMA INICIADO ---'];
  presion: number = 0;

  constructor(private bellaService: BellaService) {}

  enviarMensaje() {
    if (!this.userInput.trim()) return;

    this.history.push(`Uziel > ${this.userInput}`);
    
    this.presion = this.bellaService.entrenar(this.userInput);
    const respuesta = this.bellaService.proyectar();
    
    this.history.push(`>>> Bella dice: ${respuesta}`);
    this.userInput = '';
  }
}
