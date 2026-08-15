import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Para el *ngFor
import { FormsModule } from '@angular/forms'; // ¡ESTO ES LO QUE FALTABA! error arreglado.
import { BellaService } from './bella.service'; // Quitamos un punto (antes ../bella.service, lo que hacía que veamos hacia atrás, en lugar hacia adelante)

@Component({
  selector: 'app-bella-terminal',
  standalone: true, // Esto confirma que no necesita módulo (modo estándar)
  imports: [CommonModule, FormsModule], // <--- IMPORTANTE: Lucas necesita esto aquí
  templateUrl: './bella-terminal.component.html',
  styleUrls: ['./bella-terminal.component.css']
})
export class BellaTerminalComponent {
  userInput: string = '';
  history: string[] = ['--- SISTEMA INICIADO ---'];
  presion: number = 0;

  constructor(private bellaService: BellaService) {}

  enviarMensaje() {
    if (!this.userInput.trim()) return;

    this.history.push(`Uziel > ${this.userInput}`);
    
    // Entrenamos y proyectamos
    this.presion = this.bellaService.entrenar(this.userInput);
    const respuesta = this.bellaService.proyectar();
    
    this.history.push(`>>> Bella dice: ${respuesta}`);
    this.userInput = ''; 
  }
}
