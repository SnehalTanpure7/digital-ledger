const navigation = [
  ['/dashboard.html', 'bi-grid-1x2', 'Dashboard'],
  ['/customers.html', 'bi-people', 'Customers'],
  ['/pending.html', 'bi-hourglass-split', 'Pending'],
  ['/completed.html', 'bi-check2-circle', 'Completed'],
  ['/history.html', 'bi-clock-history', 'History'],
  ['/notifications.html', 'bi-bell', 'Notifications']
];


function sidebarMarkup() {

  const current = location.pathname.split('/').pop() || 'dashboard.html';

  return `
    <a class="brand brand-light" href="/dashboard.html">

      <span class="brand-mark">
        <i class="bi bi-journal-check"></i>
      </span>

      <span>Smart Khata</span>

    </a>


    <nav class="sidebar-nav">

      ${navigation.map(([href, icon, text]) => {

        const page = href.split('/').pop();

        return `
          <a href="${href}"
             class="${current === page ? 'active' : ''}">

            <i class="bi ${icon}"></i>

            ${text}

          </a>
        `;

      }).join('')}

    </nav>


    <div class="sidebar-bottom">

      <hr>


      <a href="/profile.html"
         class="${current === 'profile.html' ? 'active' : ''}">

        <i class="bi bi-person-circle"></i>

        Profile

      </a>


      <a href="/index.html">

        <i class="bi bi-box-arrow-right"></i>

        Logout

      </a>

    </div>
  `;
}


document
  .querySelectorAll('[data-sidebar-content]')
  .forEach((sidebar) => {

    sidebar.innerHTML = sidebarMarkup();

  });



document
  .querySelector('.password-toggle')
  ?.addEventListener('click', (event) => {

    const input = document.querySelector('#password');

    const isPassword = input.type === 'password';

    input.type = isPassword ? 'text' : 'password';

    event.currentTarget.innerHTML =
      `<i class="bi bi-eye${isPassword ? '-slash' : ''}"></i>`;

  });
document
  .querySelector('#loginForm')
  ?.addEventListener('submit', (event) => {
    event.preventDefault();
    window.location.href = '/dashboard.html';
  });