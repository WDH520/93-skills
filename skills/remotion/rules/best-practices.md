# Remotion 最佳实践

## 动画原则

1. **动画驱动**: 始终使用 `useCurrentFrame()` 驱动动画，禁止使用CSS动画
2. **时间计算**: 以秒为单位思考，乘以fps转换为帧
3. **类型安全**: 使用 `type` 而非 `interface` 定义props
4. **性能优化**: 使用 `Sequence` 分割复杂场景
5. **资源管理**: 使用 `staticFile()` 引用本地资源

## 渲染命令

```bash
# 启动开发服务器
npx remotion studio

# 渲染视频
npx remotion render src/index.ts MyVideo output.mp4

# 渲染静态图
npx remotion still src/index.ts MyStill output.png

# 添加转场库
npx remotion add @remotion/transitions

# 添加3D支持
npx remotion add @remotion/three

# 添加Lottie支持
npx remotion add @remotion/lottie
```

## 相关链接

- [Remotion官方文档](https://www.remotion.dev/)
- [GitHub仓库](https://github.com/remotion-dev/remotion)
