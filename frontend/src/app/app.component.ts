import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  title = 'Proyecto06 - Frontend Angular';
  backendData: any = null;
  loading = false;
  error: string | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fetchBackendData();
  }

  fetchBackendData() {
    this.loading = true;
    this.error = null;
    
    // Conectar al backend (asumiendo que está en backend-service)
    this.http.get('/api/data').subscribe(
      (data: any) => {
        this.backendData = data;
        this.loading = false;
      },
      (error: any) => {
        this.error = 'Error conectando al backend: ' + error.message;
        this.loading = false;
      }
    );
  }
}
