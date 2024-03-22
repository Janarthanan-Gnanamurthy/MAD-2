<template>
  <div>
    <h2>{{ ebook.title }}</h2>
    <canvas ref="pdfCanvas"></canvas>
  </div>
</template>

<script>
import pdfjsLib from 'pdfjs-dist';

export default {
  data() {
    return {
      ebook: null,
      pdfDoc: null,
      pageNum: 1,
      pageRendering: false,
      pageNumPending: null,
      scale: 1.5,
      canvas: null,
      ctx: null
    };
  },
  methods: {
    renderPDF() {
      let pdfPath = `/assets/demo.pdf`;
      pdfjsLib.getDocument(pdfPath).promise
        .then(pdfDoc_ => {
          this.pdfDoc = pdfDoc_;
          this.canvas = this.$refs.pdfCanvas;
          this.ctx = this.canvas.getContext('2d');
          this.renderPage(this.pageNum);
        })
        .catch(error => {
          console.error('Error loading PDF:', error);
        });
    },
    renderPage(num) {
      this.pageRendering = true;
      this.pdfDoc.getPage(num).then(page => {
        let viewport = page.getViewport({ scale: this.scale });
        this.canvas.height = viewport.height;
        this.canvas.width = viewport.width;

        let renderContext = {
          canvasContext: this.ctx,
          viewport: viewport
        };
        page.render(renderContext).promise.then(() => {
          this.pageRendering = false;
          if (this.pageNumPending !== null) {
            this.renderPage(this.pageNumPending);
            this.pageNumPending = null;
          }
        });
      }).catch(error => {
        console.error('Error rendering page:', error);
      });

      this.$nextTick(() => {
        this.$refs.pdfCanvas.addEventListener('click', this.onCanvasClick);
      });
    },
    onCanvasClick(event) {
      if (this.pageRendering) {
        this.pageNumPending = this.pageNum;
      } else {
        this.pageNum++;
        if (this.pageNum <= this.pdfDoc.numPages) {
          this.renderPage(this.pageNum);
        }
      }
    }
  }
};
</script>

<style scoped>
canvas {
  border: 1px solid black;
}
</style>
