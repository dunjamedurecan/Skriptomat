import React, { useEffect, useRef, useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

const PdfViewer = ({ pdfUrl }) => {
  const canvasRef = useRef(null);
  const renderTaskRef = useRef(null);

  useEffect(() => {
    if (!pdfUrl) return;

    const loadingTask = pdfjsLib.getDocument(pdfUrl);

    loadingTask.promise.then(pdf => {
      pdf. getPage(1).then(page => {
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
  }, [pdfUrl]);

  return <canvas ref={canvasRef} style={{ border: '1px solid black', width: '100%' }} />;
};

export default PdfViewer;