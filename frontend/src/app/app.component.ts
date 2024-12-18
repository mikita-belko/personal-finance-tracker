import { Component } from '@angular/core';
import { FinanceDashboardComponent } from './components/finance-dashboard/finance-dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FinanceDashboardComponent], // Импорт компонента
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {}
