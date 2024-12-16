import express from 'express';
import bodyParser from 'body-parser';
import fs from 'fs';
import path from 'path';

const app = express();

// 手动设置 CORS 头
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
});

// 使用 body-parser 来解析 JSON 请求体
app.use(bodyParser.json());

// 模拟的预测函数
const predictImage = (inputImagePath) => {
  // 这里可以调用你的图像处理和预测逻辑
  // 例如，使用某个库来处理图像并返回预测结果
  return {
    "save_dir":  inputImagePath,
    "rectangle_pos": {
      "x": (Math.random() * 1000).toFixed(3),
      "y":  (Math.random() * 1000).toFixed(3),
      "width":  (Math.random() * 100).toFixed(3),
      "height":  (Math.random() * 100).toFixed(3)
    },
    "scores":  (Math.random() * 100).toFixed(2) + "%" ,
    "classes": 2,
    "inference_time":  (Math.random() * 10).toFixed(2) + "s"
  };
};

// 处理 POST 请求的路由
app.post('/predict', (req, res) => {
  const { input_image } = req.body;

  if (!input_image) {
    return res.status(400).json({ error: 'Input image path is required' });
  }

  // 检查输入的图像路径是否有效
  const inputImagePath = path.resolve(input_image);
  if (!fs.existsSync(inputImagePath)) {
    return res.status(400).json({ error: 'Input image does not exist' });
  }

  // 调用预测函数
  const predictionResult = predictImage(inputImagePath);

  // 返回预测结果
  res.json(predictionResult);
});

// 启动服务器
app.listen(8000, () => {
  console.log('Server is running on port 8000');
});
