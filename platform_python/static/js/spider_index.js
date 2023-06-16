var currentStep = 1;
var maxDepth = 3; // 最大爬取深度

function showStep(step) {
  var steps = document.getElementsByClassName("step");
  for (var i = 0; i < steps.length; i++) {
    steps[i].classList.remove("active");
  }

  document.getElementById("step" + step).classList.add("active");
}

document.getElementById("url-form").addEventListener("submit", function(event) {
  event.preventDefault();
  var url = document.getElementById("url-input").value;

  // 在这里执行爬取操作
  crawlWebsite(url, 1); // 从深度1开始爬取

  currentStep++;
  showStep(currentStep);
});

document.getElementById("next-btn").addEventListener("click", function() {
  if (currentStep < maxDepth) {
    currentStep++;
    showStep(currentStep);
    crawlWebsite("", currentStep); // 爬取下一层深度
  }
});

function crawlWebsite(url, depth) {
  // 执行爬取操作，根据提供的URL和深度进行爬取，并将结果显示在界面上
  var resultContainer = document.getElementById("result");
  resultContainer.innerHTML += "<p>深度 " + depth + " 的爬取结果...</p>";

  // 模拟异步操作，延迟1秒显示下一步按钮
  setTimeout(function() {
    document.getElementById("next-btn").style.display = "block";
  }, 1000);
}

// Show the initial step
showStep(currentStep);
