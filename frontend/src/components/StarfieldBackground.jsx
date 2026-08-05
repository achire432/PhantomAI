/**
 * PHANTOMAI STARFIELD BACKGROUND
 * ==============================
 *
 * A responsive Canvas-based cosmic background for PhantomAI.
 *
 * IMPORTANT:
 * This component is deliberately independent from the rest of the
 * PhantomAI UI. It sits behind the application and never captures
 * mouse/touch clicks.
 *
 * FIXES INCLUDED:
 *
 * 1. Browser minimize/maximize resizing
 * 2. Window resizing
 * 3. macOS fullscreen transitions
 * 4. Retina / high-DPI displays
 * 5. Temporary zero-sized viewport during minimize
 * 6. Stars getting trapped at one edge after resize
 * 7. Canvas becoming blurry on Retina displays
 * 8. Animation continuing unnecessarily while the page is hidden
 *
 * The most important fix is that stars are regenerated whenever
 * the viewport changes. This prevents stars from retaining positions
 * based on an old canvas size.
 */

import React, { useEffect, useRef } from 'react';

const StarfieldBackground = () => {
  /**
   * Reference to the actual HTML canvas element.
   *
   * React gives us access to the DOM canvas through this ref.
   */
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;

    /**
     * Safety check.
     *
     * If the canvas somehow isn't mounted yet, stop here instead
     * of causing a JavaScript error.
     */
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    let animationId = null;

    /**
     * Stores all stars currently visible.
     */
    let stars = [];

    /**
     * These represent the dimensions that the stars use.
     *
     * IMPORTANT:
     *
     * We use CSS pixels for our star coordinates.
     *
     * The actual canvas bitmap will be larger on Retina displays,
     * but ctx.setTransform() allows us to continue thinking in
     * normal CSS pixels.
     */
    let viewportWidth = 0;
    let viewportHeight = 0;

    /**
     * Used to prevent excessive resize calculations.
     *
     * Browsers can fire MANY resize events while a window is
     * being resized.
     *
     * requestAnimationFrame lets us handle the resize once per
     * visual frame instead of potentially hundreds of times.
     */
    let resizeFrame = null;

    /**
     * =========================================================
     * GET CURRENT VIEWPORT SIZE
     * =========================================================
     *
     * window.innerWidth / innerHeight normally work perfectly.
     *
     * visualViewport is useful on modern browsers because it
     * represents the currently visible viewport more accurately,
     * particularly during browser UI/fullscreen transitions.
     */
    const getViewportSize = () => {
      const width =
        window.visualViewport?.width || window.innerWidth;

      const height =
        window.visualViewport?.height || window.innerHeight;

      return {
        width: Math.max(1, Math.floor(width)),
        height: Math.max(1, Math.floor(height)),
      };
    };

    /**
     * =========================================================
     * CREATE STARS
     * =========================================================
     *
     * Every time the viewport changes significantly, we create
     * a fresh star distribution.
     *
     * WHY?
     *
     * Imagine the browser is 1400px wide.
     *
     * A star might be at:
     *
     *     x = 1200
     *
     * Then the browser is minimized and temporarily reports:
     *
     *     width = 1
     *
     * The old star is now outside the canvas.
     *
     * If we simply resize the canvas and keep the old stars,
     * many stars can become stuck around an edge.
     *
     * Recreating them guarantees that every star starts inside
     * the CURRENT viewport.
     */
    const createStars = () => {
      stars = [];

      /**
       * You can tune this later for performance.
       *
       * 500 gives us the dense futuristic space effect we want.
       */
      const numStars = 500;

      for (let i = 0; i < numStars; i++) {
        stars.push({
          /**
           * Random position across the CURRENT viewport.
           */
          x: Math.random() * viewportWidth,
          y: Math.random() * viewportHeight,

          /**
           * Random star size.
           *
           * Small stars create depth.
           * Larger stars create occasional glowing points.
           */
          size: Math.random() * 3.5 + 0.8,

          /**
           * Very slow random movement.
           *
           * The movement is intentionally tiny.
           *
           * We don't want PhantomAI to look like a screensaver.
           * We want it to feel like the user is floating through
           * a quiet futuristic cosmos.
           */
          dx: (Math.random() - 0.5) * 0.04,
          dy: (Math.random() - 0.5) * 0.04,

          /**
           * Base brightness.
           */
          opacity: Math.random() * 0.7 + 0.3,

          /**
           * Controls the speed of the twinkle.
           */
          twinkleSpeed: Math.random() * 0.02 + 0.005,

          /**
           * Random starting point for the twinkle animation.
           *
           * Without this, all stars would brighten/dim together,
           * which would look artificial.
           */
          twinklePhase: Math.random() * Math.PI * 2,
        });
      }
    };

    /**
     * =========================================================
     * RESIZE CANVAS
     * =========================================================
     *
     * This is the most important part of the fix.
     */
    const resizeCanvas = () => {
      /**
       * Get the latest REAL viewport dimensions.
       */
      const { width, height } = getViewportSize();

      /**
       * Ignore impossible/temporary dimensions.
       *
       * During minimize/maximize, some browsers can temporarily
       * report extremely small dimensions.
       *
       * We don't want to destroy our normal canvas state based
       * on a temporary value.
       */
      if (width <= 10 || height <= 10) {
        return;
      }

      viewportWidth = width;
      viewportHeight = height;

      /**
       * =======================================================
       * DEVICE PIXEL RATIO
       * =======================================================
       *
       * Modern Macs, iPhones and many laptops have Retina/HiDPI
       * displays.
       *
       * CSS might say:
       *
       *     1440 x 900
       *
       * But the physical pixel density can be 2x.
       *
       * If we only set:
       *
       *     canvas.width = 1440
       *
       * the canvas may look blurry.
       *
       * We therefore render at a higher internal resolution while
       * keeping the visual CSS size exactly the same.
       */
      const dpr = Math.min(window.devicePixelRatio || 1, 2);

      /**
       * Internal drawing resolution.
       */
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);

      /**
       * Visual size of the canvas.
       *
       * This ensures it fills the viewport edge-to-edge.
       */
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;

      /**
       * =======================================================
       * SCALE THE DRAWING SYSTEM
       * =======================================================
       *
       * Our star positions are stored in CSS pixels.
       *
       * setTransform() tells Canvas:
       *
       * "When I say x=500, draw it at 500 CSS pixels,
       * but internally render it at the appropriate Retina
       * resolution."
       */
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      /**
       * Clear any previous drawing.
       */
      ctx.clearRect(0, 0, width, height);

      /**
       * =======================================================
       * CRITICAL FIX
       * =======================================================
       *
       * Recreate the stars based on the NEW viewport.
       *
       * This prevents the old star coordinates from becoming
       * trapped in a narrow column after minimize/maximize.
       */
      createStars();
    };

    /**
     * =========================================================
     * SCHEDULE RESIZE
     * =========================================================
     *
     * Rather than immediately resizing every time the browser
     * fires a resize event, we wait for the next animation frame.
     *
     * This is much smoother and reduces unnecessary work.
     */
    const scheduleResize = () => {
      if (resizeFrame !== null) {
        cancelAnimationFrame(resizeFrame);
      }

      resizeFrame = requestAnimationFrame(() => {
        resizeFrame = null;
        resizeCanvas();
      });
    };

    /**
     * =========================================================
     * INITIAL SETUP
     * =========================================================
     *
     * Run once when PhantomAI first loads.
     */
    resizeCanvas();

    /**
     * Normal browser resize.
     *
     * Handles:
     * - dragging the window size
     * - maximizing
     * - restoring
     * - fullscreen transitions
     */
    window.addEventListener('resize', scheduleResize);

    /**
     * visualViewport resize.
     *
     * Some browsers report viewport changes here that aren't
     * always represented exactly the same way by window.resize.
     */
    if (window.visualViewport) {
      window.visualViewport.addEventListener(
        'resize',
        scheduleResize
      );
    }

    /**
     * =========================================================
     * PAGE VISIBILITY
     * =========================================================
     *
     * When the browser window is minimized, the document can
     * become hidden.
     *
     * When it becomes visible again, force a fresh measurement.
     *
     * This is extremely important for the exact bug you described.
     */
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        /**
         * Give the browser one frame to finish restoring the
         * viewport before measuring it again.
         */
        requestAnimationFrame(() => {
          resizeCanvas();
        });
      }
    };

    document.addEventListener(
      'visibilitychange',
      handleVisibilityChange
    );

    /**
     * =========================================================
     * PAGE SHOW
     * =========================================================
     *
     * pageshow is useful when the browser restores a page from
     * its cache or restores a previous browser state.
     */
    const handlePageShow = () => {
      scheduleResize();
    };

    window.addEventListener('pageshow', handlePageShow);

    /**
     * =========================================================
     * ANIMATION LOOP
     * =========================================================
     */
    const animate = () => {
      /**
       * Don't waste CPU/GPU resources while the browser tab is
       * hidden/minimized.
       */
      if (document.visibilityState === 'hidden') {
        animationId = requestAnimationFrame(animate);
        return;
      }

      /**
       * Clear the complete current viewport.
       */
      ctx.clearRect(
        0,
        0,
        viewportWidth,
        viewportHeight
      );

      /**
       * Draw every star.
       */
      stars.forEach((star) => {
        /**
         * -----------------------------------------------------
         * FLOATING MOTION
         * -----------------------------------------------------
         */
        star.x += star.dx;
        star.y += star.dy;

        /**
         * -----------------------------------------------------
         * EDGE WRAPPING
         * -----------------------------------------------------
         *
         * IMPORTANT:
         *
         * Instead of bouncing stars against the edge, we wrap
         * them around.
         *
         * This creates a more natural infinite-space effect.
         *
         * Example:
         *
         *     star leaves right side
         *              ↓
         *     it appears on the left
         *
         * This prevents visual buildup at the edges.
         */
        if (star.x > viewportWidth + star.size) {
          star.x = -star.size;
        } else if (star.x < -star.size) {
          star.x = viewportWidth + star.size;
        }

        if (star.y > viewportHeight + star.size) {
          star.y = -star.size;
        } else if (star.y < -star.size) {
          star.y = viewportHeight + star.size;
        }

        /**
         * -----------------------------------------------------
         * TWINKLE
         * -----------------------------------------------------
         */
        star.twinklePhase += star.twinkleSpeed;

        const currentOpacity =
          star.opacity *
          (0.6 + 0.4 * Math.sin(star.twinklePhase));

        /**
         * -----------------------------------------------------
         * DRAW MAIN STAR
         * -----------------------------------------------------
         */
        ctx.beginPath();

        ctx.arc(
          star.x,
          star.y,
          star.size,
          0,
          Math.PI * 2
        );

        ctx.fillStyle = `rgba(255, 255, 255, ${currentOpacity})`;

        ctx.fill();

        /**
         * -----------------------------------------------------
         * CYAN GLOW
         * -----------------------------------------------------
         *
         * Larger stars receive a subtle PhantomAI cyan aura.
         */
        if (star.size > 2) {
          ctx.save();

          ctx.shadowColor = 'rgba(0, 212, 255, 0.15)';
          ctx.shadowBlur = 8;

          ctx.beginPath();

          ctx.arc(
            star.x,
            star.y,
            star.size * 2,
            0,
            Math.PI * 2
          );

          ctx.fillStyle = 'rgba(0, 212, 255, 0.03)';

          ctx.fill();

          ctx.restore();
        }
      });

      /**
       * Continue animation.
       */
      animationId = requestAnimationFrame(animate);
    };

    /**
     * Start the starfield.
     */
    animate();

    /**
     * =========================================================
     * CLEANUP
     * =========================================================
     *
     * React calls this when the component is removed.
     *
     * Without cleanup, multiple animation loops/listeners could
     * remain active and cause memory leaks or performance issues.
     */
    return () => {
      if (animationId !== null) {
        cancelAnimationFrame(animationId);
      }

      if (resizeFrame !== null) {
        cancelAnimationFrame(resizeFrame);
      }

      window.removeEventListener(
        'resize',
        scheduleResize
      );

      if (window.visualViewport) {
        window.visualViewport.removeEventListener(
          'resize',
          scheduleResize
        );
      }

      document.removeEventListener(
        'visibilitychange',
        handleVisibilityChange
      );

      window.removeEventListener(
        'pageshow',
        handlePageShow
      );
    };
  }, []);

  /**
   * ===========================================================
   * CANVAS ELEMENT
   * ===========================================================
   *
   * position: fixed
   * ----------------
   * Keeps the starfield attached to the viewport rather than
   * normal document flow.
   *
   * top/left: 0
   * ----------
   * Starts exactly at the upper-left corner.
   *
   * width/height: 100vw / 100vh
   * ----------------------------
   * Provides an initial full-screen CSS size.
   *
   * pointerEvents: none
   * -------------------
   * CRITICAL for PhantomAI.
   *
   * The canvas must NEVER prevent the user from clicking:
   *
   * - Login
   * - Send
   * - Settings
   * - Sidebar
   * - Chat
   * - Buttons
   *
   * zIndex: 0
   * ----------
   * Places the starfield behind the application UI.
   */
  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,

        width: '100vw',
        height: '100vh',

        margin: 0,
        padding: 0,
        border: 'none',

        display: 'block',

        /**
         * The starfield should never create a scrollbar.
         */
        overflow: 'hidden',

        /**
         * Never interfere with UI interaction.
         */
        pointerEvents: 'none',

        /**
         * PhantomAI content will sit above this.
         */
        zIndex: 0,
      }}
    />
  );
};

export default StarfieldBackground;