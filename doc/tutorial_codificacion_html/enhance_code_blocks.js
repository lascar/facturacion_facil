// Enhanced code block functionality for Advanced Coding Tutorial
// Provides copy functionality, syntax highlighting, and language detection

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
            } else if (language === 'python') {
                pre.classList.add('python');
            } else if (language === 'html') {
                pre.classList.add('html');
            } else if (language === 'css') {
                pre.classList.add('css');
            }
        }
        
        // Add line numbers for long code blocks
        if (code && code.textContent.split('\n').length > 10) {
            pre.classList.add('line-numbers');
        }
        
        // Add copy button
        addCopyButton(pre);
    });
}

function addCopyButton(preElement) {
    const copyButton = document.createElement('button');
    copyButton.innerHTML = '📋';
    copyButton.className = 'copy-button';
    copyButton.style.cssText = `
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(52, 152, 219, 0.8);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 5px 8px;
        cursor: pointer;
        font-size: 14px;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 10;
    `;
    
    preElement.style.position = 'relative';
    preElement.appendChild(copyButton);
    
    // Show button on hover
    preElement.addEventListener('mouseenter', () => {
        copyButton.style.opacity = '1';
    });
    
    preElement.addEventListener('mouseleave', () => {
        copyButton.style.opacity = '0';
    });
    
    // Copy functionality
    copyButton.addEventListener('click', (e) => {
        e.stopPropagation();
        copyCodeToClipboard(preElement);
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
        console.error('Fallback: Unable to copy', err);
    }
    
    document.body.removeChild(textArea);
}

function showCopyFeedback(preElement) {
    // Create temporary feedback element
    const feedback = document.createElement('div');
    feedback.textContent = '✅ ¡Copiado!';
    feedback.style.cssText = `
        position: absolute;
        top: 10px;
        right: 50px;
        background: #28a745;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
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
    
    preElement.appendChild(feedback);
    
    setTimeout(() => {
        if (feedback.parentNode) {
            feedback.parentNode.removeChild(feedback);
        }
    }, 2000);
}

function detectLanguage(code) {
    const lowerCode = code.toLowerCase();
    
    // Python detection (enhanced)
    if ((code.includes('class ') && code.includes('def ') && code.includes('self')) ||
        code.includes('import ') || code.includes('from ') || 
        lowerCode.includes('python') || code.includes('__init__') ||
        code.includes('#!/usr/bin/env python') || code.includes('# -*- coding: utf-8 -*-')) {
        return 'python';
    }
    
    // JavaScript detection
    if ((code.includes('function') && (code.includes('var ') || code.includes('const ') || code.includes('let '))) ||
        code.includes('console.log') || code.includes('document.') || code.includes('window.') ||
        code.includes('addEventListener')) {
        return 'javascript';
    }
    
    // SQL detection (enhanced)
    if (lowerCode.includes('select') && lowerCode.includes('from') ||
        lowerCode.includes('insert into') || lowerCode.includes('update ') || 
        lowerCode.includes('delete from') || lowerCode.includes('create table') ||
        lowerCode.includes('alter table') || lowerCode.includes('drop table')) {
        return 'sql';
    }
    
    // HTML detection
    if (code.includes('<!DOCTYPE') || code.includes('<html') || 
        (code.includes('<') && code.includes('>') && code.includes('</'))) {
        return 'html';
    }
    
    // CSS detection
    if ((code.includes('{') && code.includes('}') && code.includes(':')) ||
        code.includes('@media') || code.includes('background:') || code.includes('color:') ||
        code.includes('@import') || code.includes('font-family:')) {
        return 'css';
    }
    
    // JSON detection (enhanced)
    if ((code.trim().startsWith('{') && code.trim().endsWith('}')) ||
        (code.trim().startsWith('[') && code.trim().endsWith(']'))) {
        try {
            JSON.parse(code);
            return 'json';
        } catch (e) {
            // Not valid JSON, continue checking
        }
    }
    
    // Bash/Terminal detection (enhanced)
    if (code.includes('$ ') || code.includes('cd ') || code.includes('ls ') ||
        code.includes('mkdir ') || code.includes('pip install') || code.includes('npm install') ||
        code.includes('#!/bin/bash') || code.includes('chmod +x') || code.includes('sudo ')) {
        return 'bash';
    }
    
    // Configuration files
    if (code.includes('[') && code.includes(']') && code.includes('=') && 
        !code.includes('{') && !code.includes('}')) {
        return 'config';
    }
    
    return 'code';
}

// Advanced syntax highlighting for Python
function applySyntaxHighlighting() {
    document.querySelectorAll('pre[data-lang="python"] code').forEach(codeBlock => {
        let html = codeBlock.innerHTML;
        
        // Python keywords
        const keywords = ['def', 'class', 'import', 'from', 'if', 'else', 'elif', 'for', 'while', 
                         'try', 'except', 'finally', 'with', 'as', 'return', 'yield', 'lambda',
                         'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False', 'self'];
        
        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            html = html.replace(regex, `<span style="color: #e74c3c; font-weight: bold;">${keyword}</span>`);
        });
        
        // Strings
        html = html.replace(/(["'])((?:\\.|(?!\1)[^\\])*?)\1/g, 
            '<span style="color: #27ae60;">$1$2$1</span>');
        
        // Comments
        html = html.replace(/(#.*$)/gm, '<span style="color: #95a5a6; font-style: italic;">$1</span>');
        
        // Numbers
        html = html.replace(/\b(\d+\.?\d*)\b/g, '<span style="color: #f39c12;">$1</span>');
        
        codeBlock.innerHTML = html;
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCodeBlocks();
    // Disable syntax highlighting to prevent HTML tag display issues
    // applySyntaxHighlighting();
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
