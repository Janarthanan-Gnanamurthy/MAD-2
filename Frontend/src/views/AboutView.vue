<template>
  <div>
    <h2>Ebook Viewer</h2>
    <object data="../assets/demo.pdf" type="application/pdf" width="100%" height="800px">
      <p>Your browser doesn't support the &lt;object&gt; element.</p>
    </object>
  </div>
</template>

<script>
export default {
  name: 'EbookViewer',
  data() {
    return {
      fileUrl: '@/assets/demo.pdf'
    }
  }
}
</script>