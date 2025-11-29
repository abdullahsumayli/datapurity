import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import apiClient from '../../config/apiClient'

interface UsageBucket {
  used: number
  limit: number
  percentage: number
}

interface Subscription {
  plan: string
  status: string
  current_period_end: string
  usage: {
    cleaning: UsageBucket
    ocr: UsageBucket
    records_per_file_limit: number
    users_limit: number
  }
  pricing?: {
    extra_card_price: number
  }
  auto_renew?: boolean
}

interface Invoice {
  id: string
  amount: number
  status: string
  date: string
  invoice_url: string
}

function BillingPage() {
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBillingData()
  }, [])

  const fetchBillingData = async () => {
    try {
      const [subResponse, invoicesResponse] = await Promise.all([
        apiClient.get('/billing/subscription'),
        apiClient.get('/billing/invoices')
      ])
      setSubscription(subResponse.data)
      setInvoices(invoicesResponse.data)
    } catch (error) {
      console.error('Failed to fetch billing data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getPlanName = (plan: string) => {
    const plans: Record<string, string> = {
      free: 'ظ…ط¬ط§ظ†ظٹ',
      starter: 'ظ…ط¨طھط¯ط¦',
      professional: 'ظ…ط­طھط±ظپ',
      enterprise: 'ظ…ط¤ط³ط³ط§طھ'
    }
    return plans[plan] || plan
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">ط¬ط§ط±ظٹ ط§ظ„طھط­ظ…ظٹظ„...</div>
      </div>
    )
  }

  const usagePercentage = subscription
    ? subscription.usage.cleaning?.percentage ?? 0
    : 0

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>ط§ظ„ظپظˆطھط±ط© ظˆط§ظ„ط§ط´طھط±ط§ظƒ</h1>
        <p className="page-description">
          ط¥ط¯ط§ط±ط© ط§ط´طھط±ط§ظƒظƒ ظˆظ…ط¹ظ„ظˆظ…ط§طھ ط§ظ„ط¯ظپط¹
        </p>
      </div>

      {subscription && (
        <>
          <div className="subscription-card">
            <div className="plan-header">
              <div>
                <h2>ط§ظ„ط®ط·ط©: {getPlanName(subscription.plan)}</h2>
                <p className="plan-status">
                  ط§ظ„ط­ط§ظ„ط©: <span className={`status-${subscription.status}`}>
                    {subscription.status === 'active' ? 'ظ†ط´ط·' : subscription.status}
                  </span>
                </p>
              </div>
              <Link to="/checkout?plan=starter" className="btn-primary">
                طھط±ظ‚ظٹط© ط§ظ„ط¨ط§ظ‚ط©
              </Link>
            </div>

            <div className="renewal-info">
              طھط¬ط¯ظٹط¯ طھظ„ظ‚ط§ط¦ظٹ ظپظٹ {new Date(subscription.current_period_end).toLocaleDateString('ar-SA')}
            </div>
          </div>

          <div className="usage-section">
            <h2>ط§ظ„ط§ط³طھط®ط¯ط§ظ…</h2>
            <div className="usage-card">
              <div className="usage-label">
                <span>ط¬ظ‡ط§طھ ط§ظ„ط§طھطµط§ظ„</span>
                <span>
                  {subscription.usage.cleaning.used.toLocaleString('ar-SA')} /{' '}
                  {subscription.usage.cleaning.limit.toLocaleString('ar-SA')}
                </span>
              </div>
              <div className="usage-bar">
                <div 
                  className="usage-fill" 
                  style={{ width: `${Math.min(usagePercentage, 100)}%` }}
                />
              </div>
              <div className="usage-percentage">
                {usagePercentage.toFixed(1)}% ظ…ظ† ط§ظ„ط­ط¯ ط§ظ„ظ…ط³ظ…ظˆط­
              </div>
              <div className="usage-note">
                بطاقات OCR: {subscription.usage.ocr.used}/{subscription.usage.ocr.limit}
              </div>
            </div>
          </div>
        </>
      )}

      <div className="invoices-section">
        <h2>ط³ط¬ظ„ ط§ظ„ظپظˆط§طھظٹط±</h2>
        <div className="invoices-table">
          <table>
            <thead>
              <tr>
                <th>ط§ظ„طھط§ط±ظٹط®</th>
                <th>ط§ظ„ظ…ط¨ظ„ط؛</th>
                <th>ط§ظ„ط­ط§ظ„ط©</th>
                <th>ط§ظ„ط¥ط¬ط±ط§ط،</th>
              </tr>
            </thead>
            <tbody>
              {invoices.length === 0 ? (
                <tr>
                  <td colSpan={4} className="no-data">ظ„ط§ طھظˆط¬ط¯ ظپظˆط§طھظٹط±</td>
                </tr>
              ) : (
                invoices.map(invoice => (
                  <tr key={invoice.id}>
                    <td>{new Date(invoice.date).toLocaleDateString('ar-SA')}</td>
                    <td>{invoice.amount.toFixed(2)} ط±ظٹط§ظ„</td>
                    <td>
                      <span className={`status-badge status-${invoice.status}`}>
                        {invoice.status === 'paid' ? 'ظ…ط¯ظپظˆط¹' : 'ظ‚ظٹط¯ ط§ظ„ط§ظ†طھط¸ط§ط±'}
                      </span>
                    </td>
                    <td>
                      <a href={invoice.invoice_url} className="btn-link" target="_blank" rel="noopener noreferrer">
                        ًں“„ ط¹ط±ط¶ ط§ظ„ظپط§طھظˆط±ط©
                      </a>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <style>{`
        .subscription-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2rem;
          border-radius: 12px;
          margin: 2rem 0;
        }

        .plan-header {
          display: flex;
          justify-content: space-between;
          align-items: start;
          margin-bottom: 1rem;
        }

        .plan-header h2 {
          color: white;
          margin: 0;
        }

        .plan-status {
          margin-top: 0.5rem;
          opacity: 0.9;
        }

        .plan-status span {
          font-weight: 600;
        }

        .renewal-info {
          opacity: 0.9;
          font-size: 0.875rem;
        }

        .usage-section {
          margin: 2rem 0;
        }

        .usage-card {
          background: white;
          padding: 1.5rem;
          border-radius: 12px;
          border: 1px solid #e5e7eb;
        }

        .usage-label {
          display: flex;
          justify-content: space-between;
          margin-bottom: 0.75rem;
          font-weight: 600;
          color: #1e40af;
        }

        .usage-bar {
          width: 100%;
          height: 24px;
          background: #f3f4f6;
          border-radius: 12px;
          overflow: hidden;
        }

        .usage-fill {
          height: 100%;
          background: linear-gradient(90deg, #10b981 0%, #059669 100%);
          transition: width 0.3s;
        }

        .usage-percentage {
          margin-top: 0.5rem;
          text-align: center;
          color: #6b7280;
          font-size: 0.875rem;
        }

        .usage-note {
          margin-top: 0.25rem;
          text-align: center;
          color: #4b5563;
          font-size: 0.85rem;
        }

        .invoices-section {
          margin-top: 3rem;
        }

        .invoices-section h2 {
          margin-bottom: 1.5rem;
        }

        .invoices-table {
          background: white;
          border-radius: 12px;
          overflow: hidden;
        }

        table {
          width: 100%;
          border-collapse: collapse;
        }

        thead {
          background: #f8f9ff;
        }

        th {
          padding: 1rem;
          text-align: right;
          font-weight: 600;
          color: #1e40af;
        }

        td {
          padding: 1rem;
          border-top: 1px solid #e5e7eb;
        }

        .no-data {
          text-align: center;
          color: #6b7280;
          padding: 3rem;
        }

        .status-badge {
          display: inline-block;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.875rem;
          font-weight: 600;
        }

        .status-paid {
          background: #d1fae5;
          color: #065f46;
        }

        .status-pending {
          background: #fef3c7;
          color: #92400e;
        }

        .btn-link {
          color: #667eea;
          text-decoration: none;
        }

        .btn-link:hover {
          text-decoration: underline;
        }

        .loading {
          text-align: center;
          padding: 3rem;
          font-size: 1.25rem;
          color: #6b7280;
        }
      `}</style>
    </div>
  )
}

export default BillingPage
