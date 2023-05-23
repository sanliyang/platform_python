function openEditModal(userId) {
  // 根据用户ID获取用户信息，并将信息填充到模态框中
  // 可以使用AJAX请求或其他方式从后端获取数据

  // 假设获取到的用户信息为以下对象
  const user = {
    id: userId,
    name: 'John Doe',
    email: 'john@example.com'
  };

  // 填充模态框中的表单
  document.getElementById('name').value = user.name;
  document.getElementById('email').value = user.email;

  // 显示模态框
  document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
  // 关闭模态框
  document.getElementById('editModal').style.display = 'none';
}


// JavaScript代码
var modal = document.getElementById('editModal');
var modalHeader = document.getElementById('modalHeader');
var isDragging = false;
var dragOffset = { x: 0, y: 0 };

modalHeader.addEventListener('mousedown', startDragging);
modalHeader.addEventListener('mouseup', stopDragging);
modalHeader.addEventListener('mousemove', dragModal);

function startDragging(event) {
  isDragging = true;
  dragOffset.x = event.clientX - modal.offsetLeft;
  dragOffset.y = event.clientY - modal.offsetTop;
}

function stopDragging() {
  isDragging = false;
}

function dragModal(event) {
  if (isDragging) {
    var left = event.clientX - dragOffset.x;
    var top = event.clientY - dragOffset.y;
    modal.style.left = left + 'px';
    modal.style.top = top + 'px';
  }
}
