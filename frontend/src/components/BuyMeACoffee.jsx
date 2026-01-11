import React, { useState, useEffect, useRef } from 'react';
import { FaCoffee, FaTimes } from 'react-icons/fa';
import styles from '../styles/BuyMeACoffee.module.css';

/**
 * Buy Me a Coffee component with PayPal JS SDK integration
 * Shows a coffee icon button that opens PayPal donation modal when clicked.
 * Only renders if the author has a paypal_email set.
 * 
 * Props:
 * - authorPaypalEmail: PayPal email of the post author
 * - authorName: Display name of the author (for thank you message)
 * - postTitle: Title of the post (optional, for reference)
 */
export default function BuyMeACoffee({ authorPaypalEmail, authorName, postTitle }) {
  const [showModal, setShowModal] = useState(false);
  const [amount, setAmount] = useState('5');
  const [customAmount, setCustomAmount] = useState('');
  const [sdkReady, setSdkReady] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const paypalRef = useRef();

  // Don't render if author doesn't accept donations
  if (!authorPaypalEmail) {
    return null;
  }

  const PAYPAL_CLIENT_ID = import.meta.env.VITE_PAYPAL_CLIENT_ID;

  // Load PayPal SDK when modal opens
  useEffect(() => {
    if (!showModal) return;

    if (window.paypal) {
      setSdkReady(true);
      return;
    }

    if (!PAYPAL_CLIENT_ID) {
      setError('PayPal nije konfiguriran. Kontaktiraj administratora.');
      return;
    }

    const script = document.createElement('script');
    script.src = `https://www.paypal.com/sdk/js?client-id=${PAYPAL_CLIENT_ID}&currency=EUR`;
    script.async = true;
    script.onload = () => setSdkReady(true);
    script.onerror = () => setError('Greška pri učitavanju PayPal SDK-a.');
    
    document.body.appendChild(script);

    return () => {
      // Cleanup if component unmounts
      if (script.parentNode) {
        script.parentNode.removeChild(script);
      }
    };
  }, [showModal, PAYPAL_CLIENT_ID]);

  // Render PayPal buttons when SDK is ready
  useEffect(() => {
    if (!sdkReady || !paypalRef.current || success) return;

    const donationAmount = getFinalAmount();
    if (donationAmount < 1) return;

    // Clear previous buttons
    paypalRef.current.innerHTML = '';

    window.paypal.Buttons({
      createOrder: (data, actions) => {
        return actions.order.create({
          purchase_units: [{
            amount: {
              value: donationAmount.toFixed(2),
              currency_code: 'EUR'
            },
            description: `Donacija za "${postTitle || 'objavu'}" - Skriptomat`,
            payee: {
              email_address: authorPaypalEmail
            }
          }]
        });
      },
      onApprove: async (data, actions) => {
        try {
          const details = await actions.order.capture();
          console.log('Transaction completed:', details);
          setSuccess(true);
          setError('');
          setTimeout(() => {
            setShowModal(false);
            setSuccess(false);
          }, 3000);
        } catch (err) {
          console.error('Transaction error:', err);
          setError('Greška pri obradi transakcije.');
        }
      },
      onError: (err) => {
        console.error('PayPal error:', err);
        setError('Došlo je do greške. Pokušaj ponovo.');
      },
      onCancel: () => {
        setError('Transakcija otkazana.');
      }
    }).render(paypalRef.current);

  }, [sdkReady, amount, customAmount, authorPaypalEmail, postTitle, success]);

  const predefinedAmounts = ['2', '5', '10', '20'];

  const handleAmountSelect = (value) => {
    setAmount(value);
    setCustomAmount('');
    setError('');
  };

  const handleCustomAmountChange = (e) => {
    const value = e.target.value;
    if (value === '' || (/^\d+\.?\d{0,2}$/.test(value) && parseFloat(value) <= 1000)) {
      setCustomAmount(value);
      setAmount('custom');
      setError('');
    }
  };

  const getFinalAmount = () => {
    if (amount === 'custom') {
      return parseFloat(customAmount) || 0;
    }
    return parseFloat(amount);
  };

  const handleModalOpen = () => {
    setShowModal(true);
    setError('');
    setSuccess(false);
  };

  const handleModalClose = () => {
    setShowModal(false);
    setError('');
    setSuccess(false);
    setSdkReady(false);
  };

  return (
    <>
      <button 
        className={styles.coffeeButton}
        onClick={handleModalOpen}
        title={`Kupi ${authorName || 'autoru'} kavu`}
      >
        <FaCoffee className={styles.coffeeIcon} />
        <span className={styles.coffeeText}>Kupi kavu</span>
      </button>

      {showModal && (
        <div className={styles.modalOverlay} onClick={handleModalClose}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <button className={styles.closeButton} onClick={handleModalClose}>
              <FaTimes />
            </button>
            
            <div className={styles.modalHeader}>
              <FaCoffee className={styles.modalCoffeeIcon} />
              <h3>Kupi kavu za {authorName || 'autora'}</h3>
            </div>

            {success ? (
              <div className={styles.successMessage}>
                <h4>✅ Hvala na donaciji!</h4>
                <p>Tvoja podrška mnogo znači {authorName ? `za ${authorName}` : 'autoru'}.</p>
              </div>
            ) : (
              <>
                <p className={styles.modalDescription}>
                  Podrži autora ove objave malom donacijom. Sredstva idu direktno na njihov PayPal račun.
                </p>

                <div className={styles.amountSection}>
                  <label>Odaberi iznos (EUR):</label>
                  <div className={styles.amountButtons}>
                    {predefinedAmounts.map((amt) => (
                      <button
                        key={amt}
                        className={`${styles.amountButton} ${amount === amt ? styles.amountButtonActive : ''}`}
                        onClick={() => handleAmountSelect(amt)}
                      >
                        €{amt}
                      </button>
                    ))}
                  </div>
                  
                  <div className={styles.customAmountWrapper}>
                    <label>Ili unesi svoj iznos:</label>
                    <div className={styles.customAmountInput}>
                      <span className={styles.currencySymbol}>€</span>
                      <input
                        type="text"
                        value={customAmount}
                        onChange={handleCustomAmountChange}
                        placeholder="0.00"
                        className={amount === 'custom' ? styles.inputActive : ''}
                        onFocus={() => setAmount('custom')}
                      />
                    </div>
                  </div>
                </div>

                {error && (
                  <div className={styles.errorMessage}>
                    {error}
                  </div>
                )}

                <div className={styles.totalSection}>
                  <span>Ukupno za donirati:</span>
                  <span className={styles.totalAmount}>€{getFinalAmount().toFixed(2)}</span>
                </div>

                {!sdkReady && !error && (
                  <div className={styles.loading}>
                    Učitavam PayPal...
                  </div>
                )}

                {sdkReady && getFinalAmount() >= 1 && (
                  <div ref={paypalRef} className={styles.paypalButtonContainer}></div>
                )}

                {getFinalAmount() < 1 && (
                  <p className={styles.disclaimer}>
                    Minimalni iznos donacije je €1.00
                  </p>
                )}

                <p className={styles.disclaimer}>
                  Bit ćeš preusmjeren na PayPal za sigurno plaćanje.
                  Možeš platiti PayPal računom ili karticom.
                </p>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}
