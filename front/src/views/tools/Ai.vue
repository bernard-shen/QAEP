<template>
    <div class="ai-container">
        <div class="sphere-container" ref="sphereContainer">
            <div class="tagcloud" ref="tagCloud"></div>
        </div>
        <div class="coming-soon">
            <h2>敬请期待</h2>
        </div>
    </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';

// TagCloud 类定义
class TagCloud {
    constructor(container, texts, options) {
        this.container = container;
        this.texts = texts;
        this.options = Object.assign({
            radius: 200,
            maxSpeed: 'normal',
            initSpeed: 'normal',
            direction: 135,
            keep: true
        }, options);
        this.init();
    }

    init() {
        const items = this.texts.map((text, index) => {
            const span = document.createElement('span');
            span.innerHTML = text;
            
            // 初始化位置参数
            const phi = Math.acos(-1 + (2 * index) / this.texts.length);
            const theta = Math.sqrt(this.texts.length * Math.PI) * phi;
            
            // 设置初始3D位置
            span._rx = Math.cos(theta) * Math.sin(phi);
            span._ry = Math.sin(theta) * Math.sin(phi);
            span._rz = Math.cos(phi);
            
            return span;
        });

        items.forEach(item => {
            this.container.appendChild(item);
            const rect = item.getBoundingClientRect();
            item._width = rect.width;
            item._height = rect.height;
            item.style.position = 'absolute';
        });

        this.width = this.container.offsetWidth;
        this.height = this.container.offsetHeight;
        this.items = items;
        this.active = false;

        this.rotate = this.rotate.bind(this);
        this.resize = this.resize.bind(this);

        window.addEventListener('resize', this.resize);
        this.mouseX = this.width / 2;
        this.mouseY = this.height / 2;

        this.container.addEventListener('mousemove', e => {
            const rect = this.container.getBoundingClientRect();
            this.mouseX = e.clientX - rect.left;
            this.mouseY = e.clientY - rect.top;
        });

        this.start();
        this.update();
    }

    start() {
        if (!this.active) {
            this.active = true;
            this.rotate();
        }
    }

    rotate() {
        if (!this.active) return;
        requestAnimationFrame(this.rotate);
        this.update();
    }

    update() {
        this.rotationAngle = (this.rotationAngle || 0) + 0.002;
        
        this.items.forEach(item => {
            // 自动旋转，不依赖鼠标位置
            const rx = item._rx * Math.cos(this.rotationAngle) - item._rz * Math.sin(this.rotationAngle);
            const rz = item._rx * Math.sin(this.rotationAngle) + item._rz * Math.cos(this.rotationAngle);
            
            const ry = item._ry;
            
            const per = this.depth(rx, ry);
            
            // 增大移动范围
            item._x = this.width / 2 + rx * this.options.radius * 1.2;
            item._y = this.height / 2 + ry * this.options.radius * 1.2;
            item._z = this.options.radius * per * 1.2;
            
            // 增大缩放范围
            const scale = 1 + per * 1;
            const alpha = 0.3 + per * 0.7;
            const color = Math.round(255 - per * 200);
            
            item.style.transform = `translate3d(${item._x - item._width / 2}px, ${item._y - item._height / 2}px, ${item._z}px) scale(${scale})`;
            item.style.opacity = alpha;
            item.style.color = `rgb(${color}, ${color}, ${color})`;
            item.style.fontSize = '20px';
            item.style.zIndex = Math.round(per * 10000);
        });
    }

    depth(x, y) {
        const dist = Math.sqrt(x * x + y * y);
        return dist < 1 ? Math.sqrt(1 - dist * dist) : 0;
    }

    resize() {
        this.width = this.container.offsetWidth;
        this.height = this.container.offsetHeight;
    }

    destroy() {
        this.active = false;
        window.removeEventListener('resize', this.resize);
    }
}

export default defineComponent({
    name: 'Ai',
    setup() {
        const tagCloud = ref(null);
        const sphereContainer = ref(null);

        // AI相关的关键词
        const texts = [
            'ChatGPT', 'AI', 'Machine Learning', 'Deep Learning', 'Neural Networks',
            'NLP', 'Computer Vision', 'Robotics', 'Data Science', 'Automation',
            'Big Data', 'Algorithm', 'Python', 'TensorFlow', 'PyTorch',
            'OpenAI', 'Artificial Intelligence', 'GPT-3', 'BERT', 'Transformer',
            'RNN', 'CNN', 'LSTM', 'Reinforcement Learning', 'AGI',
            'MLOps', 'AI Ethics', 'Computer Science', 'Innovation', 'Future'
        ];

        onMounted(() => {
            if (tagCloud.value && sphereContainer.value) {
                const cloud = new TagCloud(tagCloud.value, texts, {
                    radius: Math.min(sphereContainer.value.offsetWidth, sphereContainer.value.offsetHeight) / 2.5, // 增大半径
                    maxSpeed: 'normal',
                    initSpeed: 'normal',
                    direction: 135,
                    keep: true
                });

                // 确保容器有初始大小
                sphereContainer.value.style.minHeight = '500px';
            }
        });

        return {
            tagCloud,
            sphereContainer
        };
    }
});
</script>

<style lang="less" scoped>
.ai-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    background: #1a1a1a;
    color: #fff;

    .sphere-container {
        width: 100%;
        height: 60vh;
        display: flex;
        justify-content: center;
        align-items: center;

        .tagcloud {
            width: 100%;
            height: 100%;
            position: relative;

            span {
                cursor: pointer;
                font-weight: bold;
                font-family: 'Arial', sans-serif;
                transition: transform 0.3s, opacity 0.3s;

                &:hover {
                    color: #00ff00 !important;
                    transform: scale(1.2) !important;
                }
            }
        }
    }

    .coming-soon {
        margin-top: 40px;
        text-align: center;

        h2 {
            font-size: 32px;
            color: #00ff00;
            text-transform: uppercase;
            letter-spacing: 4px;
            animation: pulse 2s infinite;
        }
    }
}

@keyframes pulse {
    0% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
    100% {
        opacity: 1;
    }
}
</style>
