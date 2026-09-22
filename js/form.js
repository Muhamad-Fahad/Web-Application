/**
 * CyberTech Employee Registration & Records Engine
 * Handles real-time validation, dynamic metrics, and persistent storage
 */

const STORAGE_KEY = 'cybertech_employees_records';

// Initial seed data if storage is empty
const INITIAL_RECORDS = [
  {
    id: '10482',
    name: 'Elena Rostova',
    email: 'elena.rostova@cybertech.net',
    phone: '4155550198',
    dept: 'Cybersecurity Operations',
    clearance: 'Tier 5 - Root Admin',
    salary: '165000',
    workMode: 'Hybrid',
    registeredAt: '2026-03-15'
  },
  {
    id: '20931',
    name: 'Marcus Chen',
    email: 'marcus.chen@cybertech.net',
    phone: '2065550143',
    dept: 'AI & Neural Systems',
    clearance: 'Tier 4 - High Clearance',
    salary: '182000',
    workMode: 'Remote',
    registeredAt: '2026-05-20'
  },
  {
    id: '30412',
    name: 'Aria Thorne',
    email: 'aria.thorne@cybertech.net',
    phone: '3125550876',
    dept: 'Quantum Infrastructure',
    clearance: 'Tier 3 - Standard Field',
    salary: '148000',
    workMode: 'On-Site',
    registeredAt: '2026-08-11'
  }
];

// In-memory / localStorage manager
const RecordsManager = {
  getAll() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      if (!data) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_RECORDS));
        return INITIAL_RECORDS;
      }
      return JSON.parse(data);
    } catch (e) {
      console.error('Storage read error:', e);
      return INITIAL_RECORDS;
    }
  },

  add(record) {
    const records = this.getAll();
    records.unshift(record);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
    return records;
  },

  delete(id) {
    let records = this.getAll();
    records = records.filter(r => r.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
    return records;
  }
};

// UI Toast Notification Provider
function showNotification(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '✔' : '✖'}</span>
    <span style="font-size: 0.88rem;">${message}</span>
  `;
  container.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add('show'));

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 4000);
}

// Form Validation Logic
const FormValidator = {
  rules: {
    // 1. Full Name: empty check + alphanumeric/name characters
    fullName(val) {
      if (!val || !val.trim()) return 'Employee full name cannot be empty.';
      if (val.trim().length < 3) return 'Name must be at least 3 characters.';
      if (!/^[a-zA-Z0-9\s'.-]+$/.test(val.trim())) return 'Name must contain valid characters.';
      return null;
    },

    // 2. Email: empty check + strict regex
    empEmail(val) {
      if (!val || !val.trim()) return 'Email address cannot be empty.';
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(val.trim())) return 'Invalid email format (e.g. name@cybertech.net).';
      return null;
    },

    // 3. Numeric: Employee ID (integer numeric validation)
    empId(val) {
      if (!val || !val.trim()) return 'Employee ID cannot be empty.';
      if (!/^\d+$/.test(val.trim())) return 'Invalid numeric input: ID must contain digits only.';
      const num = parseInt(val.trim(), 10);
      if (num < 1000 || num > 999999) return 'Employee ID must be between 1000 and 999999.';
      return null;
    },

    // 4. Password: empty check + password length >= 8
    empPassword(val) {
      if (!val || !val.trim()) return 'Access passcode cannot be empty.';
      if (val.length < 8) return 'Password-length validation: Minimum 8 characters required.';
      return null;
    },

    // 5. Numeric: Phone Number (numeric validation)
    empPhone(val) {
      if (!val || !val.trim()) return 'Contact phone cannot be empty.';
      const cleanPhone = val.replace(/[\s\-()]/g, '');
      if (!/^\+?\d{10,15}$/.test(cleanPhone)) {
        return 'Invalid numeric input: Enter a valid 10-15 digit phone number.';
      }
      return null;
    },

    // 6. Numeric: Salary / Compensation (numeric validation)
    empSalary(val) {
      if (!val || !val.trim()) return 'Annual compensation cannot be empty.';
      const num = Number(val.trim());
      if (isNaN(num) || num <= 0) {
        return 'Invalid numeric input: Compensation must be a positive number.';
      }
      if (num < 20000) {
        return 'Minimum base compensation must be at least 20,000 credits.';
      }
      return null;
    },

    // 7. Dropdown: Department required selection
    empDept(val) {
      if (!val || val === '') return 'Required dropdown selection: Please choose a department.';
      return null;
    },

    // 8. Dropdown: Security Clearance required selection
    empClearance(val) {
      if (!val || val === '') return 'Required dropdown selection: Please select a clearance tier.';
      return null;
    },

    // 9. Checkbox: Compliance
    complianceCheck(checked) {
      if (!checked) return 'You must acknowledge the Security & Data Compliance agreement.';
      return null;
    }
  },

  validateField(fieldName, value) {
    if (this.rules[fieldName]) {
      return this.rules[fieldName](value);
    }
    return null;
  }
};

// DOM Renderer and Event Wireup
document.addEventListener('DOMContentLoaded', () => {
  const regForm = document.getElementById('employeeRegistrationForm');
  const searchInput = document.getElementById('searchRecords');
  const recordsTableBody = document.getElementById('recordsTableBody');
  const emptyState = document.getElementById('tableEmptyState');
  const formAlertBanner = document.getElementById('formAlertBanner');
  const formAlertText = document.getElementById('formAlertText');

  // Stats Counters
  const statTotal = document.getElementById('statTotalEmployees');
  const statDepts = document.getElementById('statTotalDepts');
  const statTopClearance = document.getElementById('statTopClearance');
  const statAvgSalary = document.getElementById('statAvgSalary');

  // Update statistics
  function updateDashboardMetrics() {
    const records = RecordsManager.getAll();
    if (statTotal) statTotal.textContent = records.length;

    if (statDepts) {
      const depts = new Set(records.map(r => r.dept));
      statDepts.textContent = depts.size;
    }

    if (statTopClearance) {
      const topTiers = records.filter(r => r.clearance.includes('Tier 5') || r.clearance.includes('Tier 4'));
      statTopClearance.textContent = topTiers.length;
    }

    if (statAvgSalary) {
      if (records.length === 0) {
        statAvgSalary.textContent = '$0k';
      } else {
        const total = records.reduce((acc, curr) => acc + (Number(curr.salary) || 0), 0);
        const avg = Math.round(total / records.length / 1000);
        statAvgSalary.textContent = `$${avg}k`;
      }
    }
  }

  // Render Records Table
  function renderRecords(query = '') {
    const records = RecordsManager.getAll();
    const normalizedQuery = query.toLowerCase().trim();

    const filtered = records.filter(r => {
      return r.name.toLowerCase().includes(normalizedQuery) ||
             r.email.toLowerCase().includes(normalizedQuery) ||
             r.dept.toLowerCase().includes(normalizedQuery) ||
             r.id.includes(normalizedQuery);
    });

    if (filtered.length === 0) {
      recordsTableBody.innerHTML = '';
      emptyState.style.display = 'block';
      return;
    }

    emptyState.style.display = 'none';
    recordsTableBody.innerHTML = filtered.map(r => {
      let badgeClass = 'badge-clearance-1';
      if (r.clearance.includes('5')) badgeClass = 'badge-clearance-5';
      else if (r.clearance.includes('4')) badgeClass = 'badge-clearance-4';
      else if (r.clearance.includes('3')) badgeClass = 'badge-clearance-3';

      const formattedSalary = Number(r.salary).toLocaleString();

      return `
        <tr>
          <td class="mono-text" style="color: var(--neon-green); font-weight: 700;">#${r.id}</td>
          <td style="font-weight: 600; color: var(--text-white);">${r.name}</td>
          <td class="mono-text" style="color: var(--text-muted); font-size: 0.82rem;">${r.email}</td>
          <td>${r.dept}</td>
          <td><span class="table-badge ${badgeClass}">${r.clearance}</span></td>
          <td class="mono-text" style="color: var(--neon-green);">$${formattedSalary}</td>
          <td><span class="cyber-badge" style="font-size: 0.7rem; padding: 2px 8px;">${r.workMode || 'Hybrid'}</span></td>
          <td style="text-align: right;">
            <button type="button" class="btn btn-danger btn-sm btn-delete" data-id="${r.id}" title="Remove Employee">
              ✖ Remove
            </button>
          </td>
        </tr>
      `;
    }).join('');

    // Attach delete listeners
    recordsTableBody.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        if (confirm(`Confirm revoking clearance & removing employee #${id}?`)) {
          RecordsManager.delete(id);
          renderRecords(searchInput ? searchInput.value : '');
          updateDashboardMetrics();
          showNotification(`Employee record #${id} purged successfully.`, 'success');
        }
      });
    });
  }

  // Real-time Field Validation Handler
  function setupInputValidation(inputElement, fieldName) {
    if (!inputElement) return;

    const group = document.getElementById(`group-${fieldName}`);
    const errorEl = document.getElementById(`error-${fieldName}`);

    const validate = () => {
      const val = inputElement.type === 'checkbox' ? inputElement.checked : inputElement.value;
      const error = FormValidator.validateField(fieldName, val);

      if (error) {
        if (group) {
          group.classList.add('has-error');
          group.classList.remove('is-valid');
        }
        if (errorEl) errorEl.textContent = error;
        return false;
      } else {
        if (group) {
          group.classList.remove('has-error');
          if (val && (inputElement.type !== 'checkbox' || val === true)) {
            group.classList.add('is-valid');
          }
        }
        return true;
      }
    };

    inputElement.addEventListener('input', validate);
    inputElement.addEventListener('change', validate);
    inputElement.addEventListener('blur', validate);
  }

  // Wire all form inputs
  const fieldList = [
    'fullName',
    'empEmail',
    'empId',
    'empPassword',
    'empPhone',
    'empSalary',
    'empDept',
    'empClearance',
    'complianceCheck'
  ];

  fieldList.forEach(fieldName => {
    const el = document.getElementById(fieldName);
    if (el) setupInputValidation(el, fieldName);
  });

  // Search input live filtering
  if (searchInput) {
    let lastSearchQuery = searchInput.value;
    const handleSearch = (val) => {
      lastSearchQuery = val;
      renderRecords(val);
    };

    ['input', 'change', 'keyup', 'search'].forEach(evt => {
      searchInput.addEventListener(evt, (e) => {
        handleSearch(e.target.value);
      });
    });

    // Handle programmatic clearing (e.g. WebDriver element.clear())
    setInterval(() => {
      if (searchInput.value !== lastSearchQuery) {
        handleSearch(searchInput.value);
      }
    }, 50);
  }

  // Clear Form Button
  const btnClear = document.getElementById('btnClearForm');
  if (btnClear) {
    btnClear.addEventListener('click', () => {
      regForm.reset();
      fieldList.forEach(name => {
        const grp = document.getElementById(`group-${name}`);
        if (grp) {
          grp.classList.remove('has-error');
          grp.classList.remove('is-valid');
        }
      });
      if (formAlertBanner) formAlertBanner.style.display = 'none';
      showNotification('Registration form cleared.', 'success');
    });
  }

  // Sample Data Autofill Button
  const btnSample = document.getElementById('btnSampleEmployee');
  if (btnSample) {
    btnSample.addEventListener('click', () => {
      const sampleNames = ['Kaelen Vex', 'Dr. Samantha Wu', 'Tariq Al-Mansoor', 'Nyx Sterling'];
      const sampleDepts = ['Cybersecurity Operations', 'AI & Neural Systems', 'Quantum Infrastructure', 'Data Defense & Cryptography'];
      const sampleClearances = ['Tier 4 - High Clearance', 'Tier 5 - Root Admin', 'Tier 3 - Standard Field'];
      const randomIdx = Math.floor(Math.random() * sampleNames.length);

      const name = sampleNames[randomIdx];
      const email = name.toLowerCase().replace(/[^a-z]/g, '.') + '@cybertech.net';
      const randomId = Math.floor(10000 + Math.random() * 90000).toString();

      document.getElementById('fullName').value = name;
      document.getElementById('empEmail').value = email;
      document.getElementById('empId').value = randomId;
      document.getElementById('empPassword').value = 'CyberKey#' + randomId;
      document.getElementById('empPhone').value = '+15550' + Math.floor(100000 + Math.random() * 900000);
      document.getElementById('empSalary').value = (120000 + Math.floor(Math.random() * 60000)).toString();
      document.getElementById('empDept').value = sampleDepts[randomIdx % sampleDepts.length];
      document.getElementById('empClearance').value = sampleClearances[randomIdx % sampleClearances.length];
      document.getElementById('complianceCheck').checked = true;

      // Validate all populated inputs
      fieldList.forEach(name => {
        const el = document.getElementById(name);
        const grp = document.getElementById(`group-${name}`);
        if (grp) {
          grp.classList.remove('has-error');
          grp.classList.add('is-valid');
        }
      });

      if (formAlertBanner) formAlertBanner.style.display = 'none';
      showNotification('Sample operative data loaded.', 'success');
    });
  }

  // Form Submit Handler
  if (regForm) {
    regForm.addEventListener('submit', (e) => {
      e.preventDefault();

      let hasError = false;
      let firstErrorText = '';

      fieldList.forEach(name => {
        const inputEl = document.getElementById(name);
        const groupEl = document.getElementById(`group-${name}`);
        const errorEl = document.getElementById(`error-${name}`);

        if (inputEl) {
          const val = inputEl.type === 'checkbox' ? inputEl.checked : inputEl.value;
          const error = FormValidator.validateField(name, val);

          if (error) {
            hasError = true;
            if (groupEl) {
              groupEl.classList.add('has-error');
              groupEl.classList.remove('is-valid');
            }
            if (errorEl) errorEl.textContent = error;
            if (!firstErrorText) firstErrorText = error;
          } else {
            if (groupEl) {
              groupEl.classList.remove('has-error');
              groupEl.classList.add('is-valid');
            }
          }
        }
      });

      // Work mode radio extraction
      const checkedMode = document.querySelector('input[name="workMode"]:checked');
      const workMode = checkedMode ? checkedMode.value : 'Hybrid';

      if (hasError) {
        if (formAlertBanner) {
          formAlertBanner.style.display = 'flex';
          formAlertText.textContent = `Form validation failed: ${firstErrorText}`;
        }
        showNotification(firstErrorText, 'error');
        return;
      }

      // Hide alert if previously shown
      if (formAlertBanner) formAlertBanner.style.display = 'none';

      // Assemble new record
      const newRecord = {
        id: document.getElementById('empId').value.trim(),
        name: document.getElementById('fullName').value.trim(),
        email: document.getElementById('empEmail').value.trim(),
        phone: document.getElementById('empPhone').value.trim(),
        dept: document.getElementById('empDept').value,
        clearance: document.getElementById('empClearance').value,
        salary: document.getElementById('empSalary').value.trim(),
        workMode: workMode,
        registeredAt: new Date().toISOString().split('T')[0]
      };

      // Check ID uniqueness
      const existing = RecordsManager.getAll().find(r => r.id === newRecord.id);
      if (existing) {
        const idGroup = document.getElementById('group-empId');
        const idError = document.getElementById('error-empId');
        if (idGroup) idGroup.classList.add('has-error');
        if (idError) idError.textContent = `Employee ID #${newRecord.id} is already registered!`;
        if (formAlertBanner) {
          formAlertBanner.style.display = 'flex';
          formAlertText.textContent = `Employee ID #${newRecord.id} is already assigned. Please use a unique ID.`;
        }
        showNotification(`Employee ID #${newRecord.id} already exists.`, 'error');
        return;
      }

      // Add record to storage
      RecordsManager.add(newRecord);

      // Refresh table & statistics
      renderRecords(searchInput ? searchInput.value : '');
      updateDashboardMetrics();

      // Show success toast
      showNotification(`Employee ${newRecord.name} (ID: #${newRecord.id}) successfully enrolled!`, 'success');

      // Reset form fields
      regForm.reset();
      fieldList.forEach(name => {
        const grp = document.getElementById(`group-${name}`);
        if (grp) {
          grp.classList.remove('has-error');
          grp.classList.remove('is-valid');
        }
      });
    });
  }

  // Initial table render and stats computation
  renderRecords();
  updateDashboardMetrics();
});
