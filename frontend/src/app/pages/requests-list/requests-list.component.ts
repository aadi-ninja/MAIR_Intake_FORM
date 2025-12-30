import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { RequestService, Request } from '../../services/request.service';

@Component({
  selector: 'app-requests-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './requests-list.component.html',
  styleUrls: ['./requests-list.component.css']
})
export class RequestsListComponent implements OnInit {

  requests: Request[] = [];
  loading = true;
  errorMessage = '';

  constructor(
    private requestService: RequestService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadRequests();
  }

  loadRequests(): void {
    this.loading = true;
    this.errorMessage = '';

    this.requestService.getRequests().subscribe(
      (data: Request[]) => {
        this.requests = data;
        this.loading = false;
      },
      (error: any) => {
        this.errorMessage = 'Failed to load requests. Please try again.';
        this.loading = false;
      }
    );
  }

  getStatusClass(status?: string): string {
    switch (status) {
      case 'SUBMITTED':
        return 'status-submitted';
      case 'APPROVED':
        return 'status-approved';
      case 'REJECTED':
        return 'status-rejected';
      case 'IN_PROGRESS':
        return 'status-in-progress';
      case 'COMPLETED':
        return 'status-completed';
      default:
        return 'status-default';
    }
  }

  newRequest(): void {
    this.router.navigate(['/intake']);
  }

  viewRequest(id: number | undefined): void {
    if (id) {
      this.router.navigate(['/requests', id]);
    }
  }
}
