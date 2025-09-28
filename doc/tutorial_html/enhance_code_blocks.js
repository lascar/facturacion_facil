// Enhanced code block functionality for Technical Tutorial
// This script provides copy functionality, syntax highlighting, and language detection

function initializeCodeBlocks() {
    document.querySelectorAll('pre').forEach((pre, index) => {
        // Add copy functionality
        pre.addEventListener('click', function(e) {
            if (e.target === this || e.target.tagName === 'CODE') {
                copyCodeToClipboard(this);
            }
        });
        
        // Add language detection
        const code = pre.querySelector('code');
        if (code) {
            const text = code.textContent;
            const language = detectLanguage(text);
            pre.setAttribute('data-lang', language);
            
            // Add special styling for different languages
            if (language === 'bash' || language === 'terminal') {
                pre.classList.add('terminal');
            } else if (language === 'sql') {
                pre.classList.add('sql');
            } else if (language === 'json') {
                pre.classList.add('json');
            } else if (language === 'html') {
                pre.classList.add('html');
            } else if (language === 'css') {
                pre.classList.add('css');
            }
        }
        
        // Add line numbers for long code blocks
        if (code && code.textContent.split('\n').length > 8) {
            pre.classList.add('line-numbers');
        }
    });
}

function copyCodeToClipboard(preElement) {
    const code = preElement.querySelector('code');
    if (!code) return;
    
    const text = code.textContent;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyFeedback(preElement);
        }).catch(err => {
            console.error('Failed to copy code: ', err);
            fallbackCopyTextToClipboard(text, preElement);
        });
    } else {
        fallbackCopyTextToClipboard(text, preElement);
    }
}

function fallbackCopyTextToClipboard(text, preElement) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopyFeedback(preElement);
        }
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
    }
    
    document.body.removeChild(textArea);
}

function showCopyFeedback(preElement) {
    // Create temporary feedback element
    const feedback = document.createElement('div');
    feedback.textContent = '✅ Copied!';
    feedback.style.cssText = `
        position: absolute;
        top: 12px;
        right: 12px;
        background: #28a745;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        z-index: 1000;
        pointer-events: none;
        animation: fadeInOut 2s ease-in-out;
    `;
    
    // Add animation keyframes if not already added
    if (!document.querySelector('#copy-feedback-animation')) {
        const style = document.createElement('style');
        style.id = 'copy-feedback-animation';
        style.textContent = `
            @keyframes fadeInOut {
                0% { opacity: 0; transform: translateY(-10px); }
                20% { opacity: 1; transform: translateY(0); }
                80% { opacity: 1; transform: translateY(0); }
                100% { opacity: 0; transform: translateY(-10px); }
            }
        `;
        document.head.appendChild(style);
    }
    
    preElement.style.position = 'relative';
    preElement.appendChild(feedback);
    
    setTimeout(() => {
        if (feedback.parentNode) {
            feedback.parentNode.removeChild(feedback);
        }
    }, 2000);
}

function detectLanguage(code) {
    const lowerCode = code.toLowerCase();
    
    // Python detection
    if ((code.includes('class ') && code.includes('def ') && code.includes('self')) ||
        code.includes('import ') || code.includes('from ') || 
        lowerCode.includes('python') || code.includes('__init__')) {
        return 'python';
    }
    
    // JavaScript detection
    if ((code.includes('function') && (code.includes('var ') || code.includes('const ') || code.includes('let '))) ||
        code.includes('console.log') || code.includes('document.') || code.includes('window.')) {
        return 'javascript';
    }
    
    // SQL detection
    if (lowerCode.includes('select') && lowerCode.includes('from') ||
        lowerCode.includes('insert into') || lowerCode.includes('update ') || lowerCode.includes('delete from')) {
        return 'sql';
    }
    
    // HTML detection
    if (code.includes('<!DOCTYPE') || code.includes('<html') || 
        (code.includes('<') && code.includes('>') && code.includes('</'))) {
        return 'html';
    }
    
    // CSS detection
    if ((code.includes('{') && code.includes('}') && code.includes(':')) ||
        code.includes('@media') || code.includes('background:') || code.includes('color:')) {
        return 'css';
    }
    
    // JSON detection
    if ((code.trim().startsWith('{') && code.trim().endsWith('}')) ||
        (code.trim().startsWith('[') && code.trim().endsWith(']'))) {
        try {
            JSON.parse(code);
            return 'json';
        } catch (e) {
            // Not valid JSON
        }
    }
    
    // Bash/Terminal detection
    if (code.includes('$ ') || code.includes('cd ') || code.includes('ls ') ||
        code.includes('mkdir ') || code.includes('pip install') || code.includes('npm install')) {
        return 'bash';
    }
    
    return 'code';
}

// Advanced syntax highlighting - DISABLED to prevent HTML tag display issues
function applySyntaxHighlighting() {
    // DISABLED: The innerHTML replacement was causing HTML tags to be displayed as text
    // instead of being rendered as HTML elements, showing "keyword">, "string">, etc.

    // The issue occurs because:
    // 1. We get innerHTML (which may already be HTML-escaped)
    // 2. We add more HTML tags with replace()
    // 3. We set innerHTML back, but the browser treats the new tags as text

    console.log('Syntax highlighting disabled to prevent HTML tag display issues');

    // Alternative approach would be to:
    // 1. Use textContent instead of innerHTML to get raw text
    // 2. Apply highlighting to raw text
    // 3. Set innerHTML with the highlighted version
    // But this is complex and may interfere with existing HTML structure
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCodeBlocks();
    applySyntaxHighlighting();
});

// Also initialize on window load as fallback
window.addEventListener('load', function() {
    // Smooth page transition
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease-in-out';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
    
    // Re-initialize if needed
    if (!document.querySelector('pre[data-lang]')) {
        initializeCodeBlocks();
        applySyntaxHighlighting();
    }
});

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeCodeBlocks,
        copyCodeToClipboard,
        detectLanguage,
        applySyntaxHighlighting
    };
}
