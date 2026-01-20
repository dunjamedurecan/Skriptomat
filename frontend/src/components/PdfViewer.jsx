import React, { useEffect, useRef, useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

const PdfViewer = ({ pdfUrl }) => {
  const canvasRef = useRef(null);
  const renderTaskRef = useRef(null);
  const [numPages, setNumPages]=useState(0);
  const[page, setPage]=useState(1);

  useEffect(() => {
    if (!pdfUrl) return;

    const loadingTask = pdfjsLib.getDocument(pdfUrl);

    loadingTask.promise.then(pdf => {
        setNumPages(pdf.numPages);
      pdf. getPage(page).then(page => {
        const scale = 1.5;
        const viewport = page.getViewport({ scale });

        const canvas = canvasRef.current;
        if (! canvas) return;

        const context = canvas. getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport. width;

        // Cancel previous render if it exists
        if (renderTaskRef.current) {
          renderTaskRef.current.cancel();
        }

        const renderContext = { canvasContext: context, viewport };
        renderTaskRef.current = page.render(renderContext);
        
        renderTaskRef.current. promise.then(() => {
          renderTaskRef.current = null;
        }).catch(err => {
          if (err.name !== 'RenderingCancelledException') {
            console. error("PDF render error:", err);
          }
          renderTaskRef.current = null;
        });
      });
    }).catch(err => {
      console.error("PDF load error:", err);
    });

    // Cleanup function
    return () => {
      if (renderTaskRef.current) {
        renderTaskRef.current.cancel();
      }
    };
  }, [pdfUrl, page]);

return (
    <div>
        <canvas ref={canvasRef} style={{ border: '1px solid black', width: '100%' }} />
  {numPages>1 &&(
    <div>
    <button onClick={()=>setPage(p=>Math.max(p-1,1))}>⬅</button>
    <span>{page}/{numPages}</span>
    <button onClick={()=>setPage(p=>Math.min(p+1,numPages))}>➡</button>
    </div>
  )}
    </div>
);
};
export default PdfViewer;