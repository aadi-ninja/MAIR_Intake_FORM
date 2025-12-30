import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = 'http://127.0.0.1:8000/api';

export interface Request {
  id?: number;
  title: string;
  description: string;
  request_type: string;
  business_unit?: string;
  priority?: string;
  status?: string;
  submitted_by: number;
  created_at?: string;
  updated_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class RequestService {

  constructor(private http: HttpClient) { }

  // Create a new request
  createRequest(request: Request): Observable<any> {
    return this.http.post<any>(`${API_URL}/requests/`, request);
  }

  // Get all requests (with optional filters)
  getRequests(skip: number = 0, limit: number = 10, status?: string, userId?: number): Observable<Request[]> {
    let url = `${API_URL}/requests/?skip=${skip}&limit=${limit}`;
    if (status) url += `&status=${status}`;
    if (userId) url += `&user_id=${userId}`;
    return this.http.get<Request[]>(url);
  }

  // Get a specific request
  getRequest(id: number): Observable<Request> {
    return this.http.get<Request>(`${API_URL}/requests/${id}`);
  }

  // Get user requests
  getUserRequests(userId: number): Observable<Request[]> {
    return this.getRequests(0, 100, undefined, userId);
  }
}
