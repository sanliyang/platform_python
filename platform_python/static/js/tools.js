function toggleSubMenu(element) {
  const submenu = element.nextElementSibling;
  submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
}

// JavaScript
const sidebarItems = document.querySelectorAll('.sidebar-item1');
const contentContainer = document.getElementById('content');

sidebarItems.forEach((item) => {
  item.addEventListener('click', () => {
    const route = item.getAttribute('data-route');

    // 发起后端请求，获取页面内容
    fetch(route)
      .then((response) => response.text())
      .then((data) => {
        // 将后端返回的页面内容渲染到右侧区域
        contentContainer.innerHTML = data;
        contentContainer.style.display = 'block'; // 显示内容区域
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  });
});
