export function disableWeb3() {
  try {
    const w = window as any;
    // Avoid accidental usage of injected providers
    if (typeof w !== 'undefined') {
      if (w.ethereum) {
        try {
          // Hide ethereum object entirely to prevent detection/usage
          delete w.ethereum;
        } catch {
          w.ethereum = undefined;
        }
      }
      // Remove common globals if present
      if (w.web3) {
        try {
          delete w.web3;
        } catch {
          w.web3 = undefined;
        }
      }
      // Optionally hide ethereum object entirely
      // Commented out to avoid breaking extensions, but ensures no usage
      // w.ethereum = undefined;
    }
  } catch {
    // Swallow errors to avoid affecting app boot
  }
}
