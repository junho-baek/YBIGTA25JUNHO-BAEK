import numpytorch as npt
from numpytorch import Tensor, nn, reshape
import numpy as np


class Conv2d(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        
        fan_in = in_channels * kernel_size * kernel_size
        limit = np.sqrt(2. / fan_in)
        self.weights: Tensor = npt.rand(out_channels, in_channels, kernel_size, kernel_size) * limit
        self.bias: Tensor = npt.zeros(out_channels, requires_grad=True)
    
    def forward(self, x: Tensor) -> Tensor:
        batch_size, _, height, width = x.shape
        kh, kw = self.kernel_size, self.kernel_size
        oh, ow = height - kh + 1, width - kw + 1
        
        out = npt.zeros(batch_size, self.out_channels, oh, ow)

        for i in range(oh):
            for j in range(ow):
                x_region = x[:, :, i:i+kh, j:j+kw]
                for oc in range(self.out_channels):
                    out[:, oc, i, j] = npt.sum(x_region * self.weights[oc], axis=(1, 2, 3)) + self.bias[oc]
        
        return out
    

class MaxPool2d(nn.Module):
    def __init__(self, kernel_size: int, stride: int) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
    
    def forward(self, x: Tensor) -> Tensor:
        batch_size, channels, height, width = x.shape
        kh, kw = self.kernel_size, self.kernel_size
        sh, sw = self.stride, self.stride
        
        oh, ow = (height - kh) // sh + 1, (width - kw) // sw + 1
        out = npt.zeros(batch_size, channels, oh, ow)
        
        for i in range(oh):
            for j in range(ow):
                x_region = x[:, :, i*sh:i*sh+kh, j*sw:j*sw+kw]
                out[:, :, i, j] = npt.max(x_region, axis=(2, 3))
        
        return out
    


class MNISTClassificationModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        # CNN 계층 정의
        self.conv1 = Conv2d(1, 16, kernel_size=3)  # 첫 번째 CNN 계층
        self.pool1 = MaxPool2d(kernel_size=2, stride=2)  # 첫 번째 풀링 계층
        self.conv2 = Conv2d(16, 32, kernel_size=3)  # 두 번째 CNN 계층
        self.pool2 = MaxPool2d(kernel_size=2, stride=2)  # 두 번째 풀링 계층
        
        # MLP 계층 정의
        self.fc1 = nn.Linear(32 * 5 * 5, 128)  # 첫 번째 완전 연결 계층
        self.fc2 = nn.Linear(128, 64)  # 두 번째 완전 연결 계층
        self.fc3 = nn.Linear(64, 10, bias=False)  # 출력 계층


    def forward(self, x: Tensor) -> Tensor:
        # CNN 계층
        x = self.conv1(x)
        x = npt.relu(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = npt.relu(x)
        x = self.pool2(x)
        
        # Flattening
        x = reshape(x, (x.shape[0], -1))
        
        # MLP 계층
        x = self.fc1(x)
        x = npt.relu(x)
        x = self.fc2(x)
        x = npt.relu(x)
        logits = self.fc3(x)
        
        return logits
    
    

