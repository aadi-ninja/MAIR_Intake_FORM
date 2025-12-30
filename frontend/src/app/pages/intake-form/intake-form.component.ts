import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RequestService } from '../../services/request.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-intake-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './intake-form.component.html',
  styleUrls: ['./intake-form.component.css']
})
export class IntakeFormComponent implements OnInit {

  form!: FormGroup;
  submitted = false;
  loading = false;
  successMessage = '';
  errorMessage = '';

  requestTypes = [
    { value: 'NEW_REQUEST', label: 'New Request' },
    { value: 'CHANGE_REQUEST', label: 'Change Request' },
    { value: 'BUG_FIX', label: 'Bug Fix' }
  ];

  priorities = [
    { value: 'LOW', label: 'Low' },
    { value: 'MEDIUM', label: 'Medium' },
    { value: 'HIGH', label: 'High' }
  ];

  impacts = [
    { value: 'LOW', label: 'Low Impact' },
    { value: 'MEDIUM', label: 'Medium Impact' },
    { value: 'HIGH', label: 'High Impact' }
  ];

  statuses = [
    { value: 'NEW', label: 'New' },
    { value: 'OPEN', label: 'Open' },
    { value: 'IN_PROGRESS', label: 'In Progress' },
    { value: 'RESOLVED', label: 'Resolved' }
  ];

  constructor(
    private fb: FormBuilder,
    private requestService: RequestService,
    private router: Router
  ) {
    this.initializeForm();
  }

  ngOnInit(): void {
    // Watch for request type changes to update conditional fields
    this.form.get('request_type')?.valueChanges.subscribe((type: string) => {
      this.updateConditionalFields(type);
    });
  }

  initializeForm() {
    this.form = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      request_type: ['NEW_REQUEST', Validators.required],
      business_unit: ['', Validators.required],
      priority: ['MEDIUM', Validators.required],
      submitted_by: [1], // Default user ID (admin)
      
      // Conditional fields for CHANGE_REQUEST
      affected_systems: [''],
      implementation_plan: [''],
      rollback_plan: [''],
      change_impact: [''],
      
      // Conditional fields for BUG_FIX
      affected_module: [''],
      steps_to_reproduce: [''],
      expected_behavior: [''],
      actual_behavior: [''],
      bug_severity: [''],
      
      // Conditional field for NEW_REQUEST
      expected_outcome: ['']
    });
  }

  private updateConditionalFields(requestType: string) {
    // Reset all conditional fields
    const conditionalFields = [
      'affected_systems', 'implementation_plan', 'rollback_plan', 'change_impact',
      'affected_module', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior', 'bug_severity',
      'expected_outcome'
    ];

    conditionalFields.forEach(field => {
      const control = this.form.get(field);
      if (control) {
        control.clearValidators();
        control.setValue('');
        control.updateValueAndValidity();
      }
    });

    // Add validators based on request type
    switch (requestType) {
      case 'CHANGE_REQUEST':
        this.form.get('affected_systems')?.setValidators([Validators.required, Validators.minLength(5)]);
        this.form.get('implementation_plan')?.setValidators([Validators.required, Validators.minLength(10)]);
        this.form.get('rollback_plan')?.setValidators([Validators.required, Validators.minLength(10)]);
        this.form.get('change_impact')?.setValidators([Validators.required]);
        break;
      case 'BUG_FIX':
        this.form.get('affected_module')?.setValidators([Validators.required, Validators.minLength(3)]);
        this.form.get('steps_to_reproduce')?.setValidators([Validators.required, Validators.minLength(10)]);
        this.form.get('expected_behavior')?.setValidators([Validators.required, Validators.minLength(5)]);
        this.form.get('actual_behavior')?.setValidators([Validators.required, Validators.minLength(5)]);
        this.form.get('bug_severity')?.setValidators([Validators.required]);
        break;
      case 'NEW_REQUEST':
        this.form.get('expected_outcome')?.setValidators([Validators.required, Validators.minLength(10)]);
        break;
    }

    // Update validity for all conditional fields
    conditionalFields.forEach(field => {
      this.form.get(field)?.updateValueAndValidity();
    });
  }

  get f() { return this.form.controls; }

  isFieldRequired(fieldName: string): boolean {
    const control = this.form.get(fieldName);
    if (control?.validator) {
      const validator = control.validator({} as any);
      return validator?.['required'] === true;
    }
    return false;
  }

  shouldShowField(fieldName: string): boolean {
    const requestType = this.form.get('request_type')?.value;
    const changeRequestFields = ['affected_systems', 'implementation_plan', 'rollback_plan', 'change_impact'];
    const bugFixFields = ['affected_module', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior', 'bug_severity'];
    const newRequestFields = ['expected_outcome'];

    switch (requestType) {
      case 'CHANGE_REQUEST':
        return changeRequestFields.includes(fieldName);
      case 'BUG_FIX':
        return bugFixFields.includes(fieldName);
      case 'NEW_REQUEST':
        return newRequestFields.includes(fieldName);
      default:
        return false;
    }
  }

  getRequestTypeLabel(): string {
    const type = this.form.get('request_type')?.value;
    const typeObj = this.requestTypes.find(t => t.value === type);
    return typeObj?.label || '';
  }

  onSubmit() {
    this.submitted = true;
    this.errorMessage = '';
    this.successMessage = '';

    if (this.form.invalid) {
      this.errorMessage = 'Please fill out all required fields correctly.';
      // Scroll to top to show error message
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    this.loading = true;

    const formData = this.form.value;
    // Remove empty conditional fields from submission
    const submitData = Object.keys(formData).reduce((acc: any, key) => {
      if (formData[key] !== '') {
        acc[key] = formData[key];
      }
      return acc;
    }, {});

    this.requestService.createRequest(submitData).subscribe(
      (response: any) => {
        this.loading = false;
        this.successMessage = `Request created successfully! (ID: ${response.id})`;
        this.form.reset();
        this.submitted = false;
        this.form.patchValue({ 
          submitted_by: 1,
          request_type: 'NEW_REQUEST',
          priority: 'MEDIUM'
        });

        // Redirect to requests list after 2 seconds
        setTimeout(() => {
          this.router.navigate(['/requests']);
        }, 2000);
      },
      (error: any) => {
        this.loading = false;
        this.errorMessage = error.error?.detail || 'Error creating request. Please try again.';
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    );
  }

  reset() {
    this.form.reset();
    this.submitted = false;
    this.form.patchValue({ 
      submitted_by: 1,
      request_type: 'NEW_REQUEST',
      priority: 'MEDIUM'
    });
  }
}
