/**
 * Şirket Yönetim Sistemi - Ana JavaScript Dosyası
 */

// DOM içeriği yüklendiğinde çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltip'lerini etkinleştir
    initializeTooltips();
    
    // Form doğrulama işlemlerini etkinleştir
    initializeFormValidation();
    
    // Departman değiştiğinde pozisyonları güncelle
    setupDepartmentPositionRelation();
    
    // Tarih alanları için datepicker'ı etkinleştir
    setupDatePickers();
    
    // Tablo arama ve sıralama işlevselliğini etkinleştir
    setupTableSearch();
});

/**
 * Bootstrap tooltip'lerini başlatır
 */
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

/**
 * Form doğrulama işlevselliğini başlatır
 */
function initializeFormValidation() {
    // Tüm formları seç
    const forms = document.querySelectorAll('.needs-validation');
    
    // Her bir form için doğrulama işlemi ekle
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Departman değiştiğinde ilgili pozisyonları günceller
 */
function setupDepartmentPositionRelation() {
    const departmentSelect = document.getElementById('department_id');
    if (departmentSelect) {
        departmentSelect.addEventListener('change', function() {
            const departmentId = this.value;
            if (departmentId > 0) {
                // AJAX ile pozisyonları getir
                fetch(`/employee/get_positions/${departmentId}`)
                    .then(response => response.json())
                    .then(data => {
                        const positionSelect = document.getElementById('position_id');
                        // Mevcut seçenekleri temizle
                        positionSelect.innerHTML = '<option value="0">Seçiniz</option>';
                        
                        // Yeni pozisyonları ekle
                        data.forEach(position => {
                            const option = document.createElement('option');
                            option.value = position.id;
                            option.textContent = position.name;
                            positionSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Pozisyonlar yüklenirken hata oluştu:', error));
            }
        });
    }
}

/**
 * Tarih seçici alanlarını başlatır
 */
function setupDatePickers() {
    // Tarih seçici gerekli tüm input'ları seç
    const dateInputs = document.querySelectorAll('input[type="date"]');
    
    // Bugünün tarihini al
    const today = new Date().toISOString().split('T')[0];
    
    // Her bir tarih input'u için min ve max değer ayarla
    dateInputs.forEach(input => {
        if (input.classList.contains('future-only')) {
            input.min = today;
        } else if (input.classList.contains('past-only')) {
            input.max = today;
        }
    });
}

/**
 * Tablo arama ve sıralama işlevselliğini başlatır
 */
function setupTableSearch() {
    const searchInput = document.getElementById('table-search');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const tableBody = document.querySelector('table tbody');
            const rows = tableBody.querySelectorAll('tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
}

/**
 * İzin talebini iptal etme onayı ister
 * @param {number} leaveId - İzin talebi ID'si
 */
function confirmCancelLeave(leaveId) {
    if (confirm('Bu izin talebini iptal etmek istediğinize emin misiniz?')) {
        document.getElementById(`cancel-leave-${leaveId}`).submit();
    }
}

/**
 * Çalışanı silme onayı ister
 * @param {number} employeeId - Çalışan ID'si
 */
function confirmDeleteEmployee(employeeId) {
    if (confirm('Bu çalışanı silmek istediğinize emin misiniz?')) {
        document.getElementById(`delete-employee-${employeeId}`).submit();
    }
}

/**
 * Departmanı silme onayı ister
 * @param {number} departmentId - Departman ID'si
 */
function confirmDeleteDepartment(departmentId) {
    if (confirm('Bu departmanı silmek istediğinize emin misiniz?')) {
        document.getElementById(`delete-department-${departmentId}`).submit();
    }
}

/**
 * Pozisyonu silme onayı ister
 * @param {number} positionId - Pozisyon ID'si
 */
function confirmDeletePosition(positionId) {
    if (confirm('Bu pozisyonu silmek istediğinize emin misiniz?')) {
        document.getElementById(`delete-position-${positionId}`).submit();
    }
}

/**
 * İzin değerlendirme formunu gönderir
 * @param {string} status - İzin durumu (onaylandi/reddedildi)
 */
function submitLeaveReview(status) {
    const form = document.getElementById('leave-review-form');
    document.getElementById('status').value = status;
    form.submit();
} 