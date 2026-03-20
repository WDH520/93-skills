# Remotion 快速开始

## 1. 安装依赖

```bash
npm install remotion @remotion/cli
```

## 2. 创建基础组件

```tsx
import { AbsoluteFill, useCurrentFrame } from 'remotion';

export const MyVideo = () => {
  const frame = useCurrentFrame();
  
  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      <h1 style={{ color: 'white' }}>Frame: {frame}</h1>
    </AbsoluteFill>
  );
};
```

## 3. 注册合成

```tsx
import { registerRoot, Composition } from 'remotion';

const Root = () => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={300}
    fps={30}
    width={1920}
    height={1080}
  />
);

registerRoot(Root);
```

## 4. 启动开发服务器

```bash
npx remotion studio
```

## 扩展功能

- **添加转场库**: `npx remotion add @remotion/transitions`
- **添加3D支持**: `npx remotion add @remotion/three`
- **添加Lottie支持**: `npx remotion add @remotion/lottie`
