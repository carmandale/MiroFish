function escapeHtml(value = '') {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

function applyInlineMarkdown(value) {
  return value
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
}

export function renderSafeMarkdown(markdown = '') {
  const escaped = escapeHtml(markdown || '')
  const lines = escaped.split('\n')
  const html = []
  let inList = false

  const closeList = () => {
    if (inList) {
      html.push('</ul>')
      inList = false
    }
  }

  lines.forEach((rawLine) => {
    const line = rawLine.trimEnd()
    const trimmed = line.trim()

    if (!trimmed) {
      closeList()
      html.push('<div class="md-spacer"></div>')
      return
    }

    const headingMatch = trimmed.match(/^(#{1,3})\s+(.*)$/)
    if (headingMatch) {
      closeList()
      const level = headingMatch[1].length
      html.push(`<h${level}>${applyInlineMarkdown(headingMatch[2])}</h${level}>`)
      return
    }

    if (trimmed.startsWith('- ')) {
      if (!inList) {
        html.push('<ul>')
        inList = true
      }
      html.push(`<li>${applyInlineMarkdown(trimmed.slice(2))}</li>`)
      return
    }

    closeList()
    if (trimmed.startsWith('> ')) {
      html.push(`<blockquote>${applyInlineMarkdown(trimmed.slice(2))}</blockquote>`)
      return
    }

    html.push(`<p>${applyInlineMarkdown(trimmed)}</p>`)
  })

  closeList()
  return html.join('')
}
