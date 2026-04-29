        const DOM = {
            target: document.getElementById('render-target'),
            seedInput: document.getElementById('seed-input'),
            colorInput: document.getElementById('color-input'),
            hashMetric: document.getElementById('hash-metric'),
            specimenId: document.getElementById('specimen-id'),
            copyBtn: document.getElementById('copy-btn'),
            pngBtn: document.getElementById('png-btn'),
            embedBtn: document.getElementById('embed-btn'),
            ratioBtns: document.querySelectorAll('.ratio-btn')
        };

        const CONFIG = {
            baseResolution: 240, 
            baseExportScale: 2400, // Longest edge will be 2400px
            maxLayers: 7,
            archivalPalette: ['#8B1A1A', '#2A2520', '#7A7068', '#5A5048']
        };

        const sanitizePalette = (inputString) => {
            const rawColors = inputString.split(',');
            const validColors = [];
            const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
            
            for (const color of rawColors) {
                const trimmed = color.trim();
                if (hexRegex.test(trimmed)) validColors.push(trimmed);
            }
            return validColors.length > 0 ? validColors : CONFIG.archivalPalette;
        };

        const generateSecureHash = (inputString) => {
            const sanitizedString = inputString.replace(/[^a-zA-Z0-9\s-_.,]/g, '').trim();
            let hashValue = 0x811c9dc5; 
            for (let i = 0; i < sanitizedString.length; i++) {
                hashValue ^= sanitizedString.charCodeAt(i);
                hashValue = Math.imul(hashValue, 0x01000193);
            }
            return Math.abs(hashValue);
        };

        const generateSequenceIdentifier = (hash) => {
            const dictionary = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
            const prefix = (hash % 89) + 10;
            let suffix = "";
            let mutableHash = hash;
            for (let i = 0; i < 6; i++) {
                suffix += dictionary.charAt(mutableHash % dictionary.length);
                mutableHash = Math.floor(mutableHash / dictionary.length);
            }
            return `${prefix}-${suffix}`;
        };

        const buildGeometryPath = (cx, cy, scale, params, modFreq = 0, modAmp = 0) => {
            const [m, n1, n2, n3] = params;
            const m_div_4 = m / 4;
            const inv_n1 = -1 / n1;
            const step = (Math.PI * 2) / CONFIG.baseResolution;
            let d = "M ";
            
            for (let i = 0; i <= CONFIG.baseResolution; i++) {
                const theta = i * step;
                const m_theta_div_4 = m_div_4 * theta;
                const term1 = Math.pow(Math.abs(Math.cos(m_theta_div_4)), n2);
                const term2 = Math.pow(Math.abs(Math.sin(m_theta_div_4)), n3);
                let radius = Math.pow(term1 + term2, inv_n1);
                
                if (modFreq > 0) radius += Math.sin(theta * modFreq) * modAmp;
                
                const x = Math.round((cx + radius * scale * Math.cos(theta)) * 100) / 100;
                const y = Math.round((cy + radius * scale * Math.sin(theta)) * 100) / 100;
                d += `${x},${y}${i < CONFIG.baseResolution ? ' L ' : ''}`;
            }
            return d + " Z";
        };

        const synthesizeGeometry = (hash, currentPalette, cx, cy, viewScale) => {
            let svgMarkup = "";
            const coreSymmetry = (hash % 8) + 2;
            const coreParams = [(hash % 30) / 10 + 0.5, (hash % 40) / 10 + 0.2, ((hash >> 2) % 40) / 10 + 0.2];
            const subSymmetry = ((hash >> 4) % 12) + 3;
            const subParams = [1.2, 0.8, 1.2];

            // Normalize internal radiuses against the shortest edge of the canvas
            const scaleMultiplier = viewScale / 100;

            for (let layer = 1; layer <= CONFIG.maxLayers; layer++) {
                const layerScale = (layer / CONFIG.maxLayers) * 36 * scaleMultiplier;
                const rotationAngle = (hash % 360) + (layer * 22.5);
                const strokeWidth = Math.max(0.08, 0.25 - (layer * 0.02));
                const strokeColor = currentPalette[layer % currentPalette.length];
                
                const pathA = buildGeometryPath(cx, cy, layerScale, [coreSymmetry, ...coreParams]);
                svgMarkup += `<path d="${pathA}" fill="none" stroke="${strokeColor}" stroke-width="${strokeWidth}" transform="rotate(${rotationAngle} ${cx} ${cy})" />`;
                
                if (layer % 2 === 0) {
                    const modFreq = (hash % 6) + 2;
                    const modAmp = 0.05 * layer;
                    const secondaryColor = currentPalette[(layer + 1) % currentPalette.length];
                    const pathB = buildGeometryPath(cx, cy, layerScale * 0.75, [subSymmetry, ...subParams], modFreq, modAmp);
                    svgMarkup += `<path d="${pathB}" fill="none" stroke="${secondaryColor}" stroke-width="${strokeWidth * 0.8}" transform="rotate(${-rotationAngle * 1.5} ${cx} ${cy})" stroke-dasharray="0.3 0.6" />`;
                }
            }

            const orbitCount = (hash % 4) + 2;
            for (let orbit = 0; orbit < orbitCount; orbit++) {
                const angle = (orbit * (360 / orbitCount)) + (hash % 90);
                const rad = angle * Math.PI / 180;
                const radiusDist = (20 + (hash % 15)) * scaleMultiplier;
                const ox = Math.round((cx + radiusDist * Math.cos(rad)) * 100) / 100;
                const oy = Math.round((cy + radiusDist * Math.sin(rad)) * 100) / 100;
                
                svgMarkup += `<circle cx="${ox}" cy="${oy}" r="1.2" fill="none" stroke="${currentPalette[0]}" stroke-width="0.15" />`;
                svgMarkup += `<line x1="${cx}" y1="${cy}" x2="${ox}" y2="${oy}" stroke="${currentPalette[2]}" stroke-width="0.05" stroke-dasharray="0.2 0.8" />`;
            }

            return svgMarkup;
        };

        const getActiveRatio = () => {
            const activeBtn = document.querySelector('.ratio-btn[data-active="true"]');
            return {
                w: parseFloat(activeBtn.dataset.w),
                h: parseFloat(activeBtn.dataset.h)
            };
        };

        const parseMetadata = () => {
            const rawSeed = DOM.seedInput.value || "Archival Initial Data";
            const hash = generateSecureHash(rawSeed);
            const identifier = generateSequenceIdentifier(hash);
            const ratio = getActiveRatio();
            
            const metadata = {
                title: `Specimen ${identifier} | Geometry Vault`,
                description: `Procedural geometry specimen synthesized from sequence ${identifier}.`,
                identifier: identifier,
                hash: `0x${hash.toString(16).toUpperCase()}`,
                aspectRatio: `${ratio.w}:${ratio.h}`,
                author: "Azzar Budiyanto",
                provider: "Geometry Vault Archival Service",
                timestamp: new Date().toISOString()
            };

            // Update social tags dynamically
            const ogTitle = document.querySelector('meta[property="og:title"]');
            const ogDesc = document.querySelector('meta[property="og:description"]');
            const twTitle = document.querySelector('meta[name="twitter:title"]');
            
            if (ogTitle) ogTitle.setAttribute('content', metadata.title);
            if (ogDesc) ogDesc.setAttribute('content', metadata.description);
            if (twTitle) twTitle.setAttribute('content', metadata.title);
            
            document.title = metadata.title;

            return metadata;
        };

        const initServiceLogic = () => {
            const params = new URLSearchParams(window.location.search);
            
            if (params.get('mode') === 'embed') {
                document.body.dataset.mode = 'embed';
            }

            if (params.get('seed')) DOM.seedInput.value = params.get('seed');
            if (params.get('colors')) DOM.colorInput.value = params.get('colors');
            
            if (params.get('w') && params.get('h')) {
                DOM.ratioBtns.forEach(btn => {
                    if (btn.dataset.w === params.get('w') && btn.dataset.h === params.get('h')) {
                        DOM.ratioBtns.forEach(b => b.removeAttribute('data-active'));
                        btn.setAttribute('data-active', 'true');
                    }
                });
            }

            // postMessage interface
            window.addEventListener('message', (e) => {
                const { type, data } = e.data;
                if (type === 'UPDATE_SPECIMEN') {
                    if (data.seed) DOM.seedInput.value = data.seed;
                    if (data.colors) DOM.colorInput.value = data.colors;
                    if (data.w && data.h) {
                        DOM.ratioBtns.forEach(btn => {
                            if (btn.dataset.w == data.w && btn.dataset.h == data.h) {
                                DOM.ratioBtns.forEach(b => b.removeAttribute('data-active'));
                                btn.setAttribute('data-active', 'true');
                            }
                        });
                    }
                    renderSynthesisPipeline();
                }

                if (type === 'GET_METADATA') {
                    const metadata = parseMetadata();
                    e.source.postMessage({ type: 'METADATA_RESPONSE', data: metadata }, e.origin);
                }

                if (type === 'GET_IMAGE_URL') {
                    const svgElement = DOM.target.querySelector('svg');
                    if (svgElement) {
                        const svgData = new XMLSerializer().serializeToString(svgElement);
                        const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
                        const url = URL.createObjectURL(blob);
                        e.source.postMessage({ type: 'IMAGE_URL_RESPONSE', data: url }, e.origin);
                    }
                }
            });
        };

        const handleEmbedExport = async () => {
            const ratio = getActiveRatio();
            const baseUrl = window.location.origin + window.location.pathname;
            const embedUrl = `${baseUrl}?mode=embed&seed=${encodeURIComponent(DOM.seedInput.value)}&colors=${encodeURIComponent(DOM.colorInput.value)}&w=${ratio.w}&h=${ratio.h}`;
            const iframeCode = `<iframe src="${embedUrl}" width="500" height="500" frameborder="0" style="border:1px solid #DDD5C5; border-radius:4px;"></iframe>`;
            
            try {
                await navigator.clipboard.writeText(iframeCode);
                buttonFeedback(DOM.embedBtn, DOM.embedBtn.innerHTML, '<i class="fa-solid fa-check"></i> [ EMBED_CODE_COPIED ]');
            } catch (err) {
                console.error('Embed export failed', err);
            }
        };

        const handleMetaExport = async () => {
            const metadata = parseMetadata();
            try {
                await navigator.clipboard.writeText(JSON.stringify(metadata, null, 2));
                buttonFeedback(DOM.metaBtn, DOM.metaBtn.innerHTML, '<i class="fa-solid fa-check"></i> [ JSON_COPIED ]');
            } catch (err) {
                console.error('Meta export failed', err);
            }
        };

        const renderSynthesisPipeline = () => {
            const rawSeed = DOM.seedInput.value || "Archival Initial Data";
            const rawPalette = DOM.colorInput.value;
            const hash = generateSecureHash(rawSeed);
            const identifier = generateSequenceIdentifier(hash);
            const activePalette = sanitizePalette(rawPalette);
            
            // Update metadata whenever we render
            parseMetadata();

            // Layout Calculations based on Aspect Ratio
            const ratio = getActiveRatio();
            let viewW = 100;
            let viewH = 100;
            
            if (ratio.w > ratio.h) {
                viewH = Math.round((100 * (ratio.h / ratio.w)) * 100) / 100;
            } else if (ratio.h > ratio.w) {
                viewW = Math.round((100 * (ratio.w / ratio.h)) * 100) / 100;
            }

            const cx = Math.round((viewW / 2) * 100) / 100;
            const cy = Math.round((viewH / 2) * 100) / 100;
            const minDim = Math.min(viewW, viewH);

            const coreSymmetry = (hash % 8) + 2;
            const geometryMarkup = synthesizeGeometry(hash, activePalette, cx, cy, minDim);

            DOM.target.innerHTML = `
                <svg viewBox="0 0 ${viewW} ${viewH}" style="aspect-ratio: ${ratio.w}/${ratio.h};" xmlns="http://www.w3.org/2000/svg" class="specimen-svg w-full h-full">
                    <rect width="${viewW}" height="${viewH}" fill="transparent"></rect>
                    
                    <g opacity="0.15">
                        <circle cx="${cx}" cy="${cy}" r="${(minDim / 2) * 0.92}" fill="none" stroke="#7A7068" stroke-width="0.1" stroke-dasharray="0.2 1" />
                        <line x1="${cx}" y1="1" x2="${cx}" y2="${viewH - 1}" stroke="#7A7068" stroke-width="0.1" stroke-dasharray="0.5 1.5" />
                        <line x1="1" y1="${cy}" x2="${viewW - 1}" y2="${cy}" stroke="#7A7068" stroke-width="0.1" stroke-dasharray="0.5 1.5" />
                    </g>
                    
                    <g>${geometryMarkup}</g>

                    <text x="2" y="${viewH - 2}" font-size="1.2" font-family="'JetBrains Mono', monospace" fill="#7A7068" letter-spacing="0.1em">ID:${identifier}</text>
                    <text x="${viewW - 2}" y="3" font-size="1.2" font-family="'JetBrains Mono', monospace" fill="#7A7068" letter-spacing="0.1em" text-anchor="end">F:${coreSymmetry}</text>
                </svg>
            `;

            DOM.hashMetric.textContent = `PTR: 0x${hash.toString(16).toUpperCase().padStart(8, '0')}`;
            DOM.specimenId.textContent = `SEQ: ${identifier}`;

            // Sync URL if not in embed mode
            if (document.body.dataset.mode !== 'embed') {
                const url = new URL(window.location);
                url.searchParams.set('seed', rawSeed);
                url.searchParams.set('colors', rawPalette);
                url.searchParams.set('w', ratio.w);
                url.searchParams.set('h', ratio.h);
                window.history.replaceState({}, '', url);
            }
        };

        const createDebouncer = (callback, delay) => {
            let timerId;
            return (...args) => {
                clearTimeout(timerId);
                timerId = setTimeout(() => callback(...args), delay);
            };
        };

        const buttonFeedback = (buttonDom, originalHtml, successHtml) => {
            buttonDom.innerHTML = successHtml;
            buttonDom.classList.add('border-[#8B1A1A]', 'text-[#8B1A1A]');
            setTimeout(() => {
                buttonDom.innerHTML = originalHtml;
                buttonDom.classList.remove('border-[#8B1A1A]', 'text-[#8B1A1A]');
            }, 2000);
        };

        const handleSVGExport = async () => {
            try {
                const svgElement = DOM.target.querySelector('svg');
                if (!svgElement) throw new Error("Render missing");
                await navigator.clipboard.writeText(svgElement.outerHTML);
                buttonFeedback(DOM.copyBtn, DOM.copyBtn.innerHTML, '<i class="fa-solid fa-check"></i> [ COPIED ]');
            } catch (error) {
                console.error('Export error:', error);
            }
        };

        const handlePNGExport = () => {
            const svgElement = DOM.target.querySelector('svg');
            if (!svgElement) return;

            const originalHtml = DOM.pngBtn.innerHTML;
            DOM.pngBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> [ RENDERING ]';

            // Calculate output resolution based on active ratio
            const ratio = getActiveRatio();
            let canvasW = CONFIG.baseExportScale;
            let canvasH = CONFIG.baseExportScale;
            
            if (ratio.w > ratio.h) canvasH = Math.round(CONFIG.baseExportScale * (ratio.h / ratio.w));
            else if (ratio.h > ratio.w) canvasW = Math.round(CONFIG.baseExportScale * (ratio.w / ratio.h));

            const svgClone = svgElement.cloneNode(true);
            svgClone.setAttribute('width', canvasW);
            svgClone.setAttribute('height', canvasH);
            
            const svgData = new XMLSerializer().serializeToString(svgClone);
            const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const img = new Image();

            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = canvasW;
                canvas.height = canvasH;
                const ctx = canvas.getContext('2d');
                
                ctx.fillStyle = '#EFE9DC'; 
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvasW, canvasH);
                
                URL.revokeObjectURL(url);
                
                const pngUrl = canvas.toDataURL('image/png');
                const downloadLink = document.createElement('a');
                
                const safeFileName = DOM.specimenId.textContent.replace('SEQ: ', '').trim();
                downloadLink.download = `archival_specimen_${safeFileName}.png`;
                downloadLink.href = pngUrl;
                downloadLink.click();

                buttonFeedback(DOM.pngBtn, originalHtml, '<i class="fa-solid fa-check"></i> [ SAVED ]');
            };
            
            img.src = url;
        };

        // Event Listeners
        const renderDebounced = createDebouncer(renderSynthesisPipeline, 32);

        DOM.ratioBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                DOM.ratioBtns.forEach(b => b.removeAttribute('data-active'));
                e.target.setAttribute('data-active', 'true');
                renderSynthesisPipeline();
            });
        });

        DOM.seedInput.addEventListener('input', renderDebounced);
        DOM.colorInput.addEventListener('input', renderDebounced);
        DOM.copyBtn.addEventListener('click', handleSVGExport);
        DOM.pngBtn.addEventListener('click', handlePNGExport);
        DOM.embedBtn.addEventListener('click', handleEmbedExport);
        DOM.metaBtn.addEventListener('click', handleMetaExport);
        
        window.addEventListener('DOMContentLoaded', () => {
            initServiceLogic();
            renderSynthesisPipeline();
            initCustomCursor();
        });

        const initCustomCursor = () => {
            if (!window.matchMedia('(pointer: fine)').matches) return;

            const cursor = document.createElement('div');
            cursor.className = 'custom-cursor';
            const trail = document.createElement('div');
            trail.className = 'custom-cursor-trail';
            
            document.body.appendChild(cursor);
            document.body.appendChild(trail);

            let mouseX = -100, mouseY = -100, trailX = -100, trailY = -100;

            document.addEventListener('mousemove', (e) => {
                mouseX = e.clientX;
                mouseY = e.clientY;
                cursor.style.setProperty('--x', `${mouseX}px`);
                cursor.style.setProperty('--y', `${mouseY}px`);
            });

            const animateTrail = () => {
                trailX += (mouseX - trailX) * 0.25;
                trailY += (mouseY - trailY) * 0.25;
                trail.style.setProperty('--x', `${trailX}px`);
                trail.style.setProperty('--y', `${trailY}px`);
                requestAnimationFrame(animateTrail);
            };
            requestAnimationFrame(animateTrail);

            const updateInteractables = () => {
                document.querySelectorAll('a, button, input, .ratio-btn').forEach(el => {
                    if (el.dataset.cursorHover) return;
                    el.dataset.cursorHover = 'true';
                    
                    el.addEventListener('mouseenter', () => {
                        cursor.classList.add('hover');
                        trail.classList.add('hover');
                    });
                    el.addEventListener('mouseleave', () => {
                        cursor.classList.remove('hover');
                        trail.classList.remove('hover');
                    });
                });
            };
            
            updateInteractables();
            
            const observer = new MutationObserver(() => updateInteractables());
            observer.observe(document.body, { childList: true, subtree: true });
        };
