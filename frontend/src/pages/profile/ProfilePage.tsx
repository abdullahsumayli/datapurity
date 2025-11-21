import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './profile.css';

interface UserProfile {
  id: number;
  email: string;
  full_name: string;
  phone?: string;
  company?: string;
  job_title?: string;
  created_at: string;
}

interface ProfileStats {
  total_cards: number;
  total_contacts: number;
  total_datasets: number;
  last_activity: string;
}

const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [stats, setStats] = useState<ProfileStats | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'activity'>('profile');
  
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    company: '',
    job_title: ''
  });

  useEffect(() => {
    loadProfile();
    loadStats();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadProfile = async () => {
    try {
      // Mock data - replace with actual API call
      const mockProfile: UserProfile = {
        id: 1,
        email: user?.email || 'user@example.com',
        full_name: user?.email?.split('@')[0] || 'المستخدم',
        phone: '+966 50 123 4567',
        company: 'شركة DataPurity',
        job_title: 'مدير تقنية المعلومات',
        created_at: new Date().toISOString()
      };
      
      setProfile(mockProfile);
      setFormData({
        full_name: mockProfile.full_name,
        email: mockProfile.email,
        phone: mockProfile.phone || '',
        company: mockProfile.company || '',
        job_title: mockProfile.job_title || ''
      });
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      // Mock data - replace with actual API call
      const mockStats: ProfileStats = {
        total_cards: 156,
        total_contacts: 892,
        total_datasets: 24,
        last_activity: new Date().toISOString()
      };
      
      setStats(mockStats);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      // Mock save - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (profile) {
        setProfile({
          ...profile,
          ...formData
        });
      }
      
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to save profile:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (profile) {
      setFormData({
        full_name: profile.full_name,
        email: profile.email,
        phone: profile.phone || '',
        company: profile.company || '',
        job_title: profile.job_title || ''
      });
    }
    setIsEditing(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('ar-SA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  };

  if (loading) {
    return (
      <div className="profile-loading">
        <div className="loading-spinner"></div>
        <p>جاري تحميل الملف الشخصي...</p>
      </div>
    );
  }

  return (
    <div className="profile-page">
      {/* Header Section */}
      <div className="profile-header">
        <div className="profile-header-content">
          <div className="profile-avatar">
            <div className="avatar-circle">
              <span className="avatar-initials">
                {profile?.full_name.charAt(0).toUpperCase() || 'M'}
              </span>
            </div>
            <button className="avatar-upload-btn">
              <span className="icon">📷</span>
              تغيير الصورة
            </button>
          </div>
          
          <div className="profile-header-info">
            <h1>{profile?.full_name}</h1>
            <p className="profile-email">{profile?.email}</p>
            <p className="profile-member-since">
              عضو منذ {profile && formatDate(profile.created_at)}
            </p>
          </div>

          {!isEditing && (
            <button className="btn-edit-profile" onClick={() => setIsEditing(true)}>
              <span className="icon">✏️</span>
              تعديل الملف الشخصي
            </button>
          )}
        </div>

        {/* Stats Cards */}
        <div className="profile-stats">
          <div className="stat-card">
            <div className="stat-icon card-icon">🎴</div>
            <div className="stat-content">
              <h3>{stats?.total_cards || 0}</h3>
              <p>بطاقة معالجة</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon contact-icon">👥</div>
            <div className="stat-content">
              <h3>{stats?.total_contacts || 0}</h3>
              <p>جهة اتصال</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon dataset-icon">📊</div>
            <div className="stat-content">
              <h3>{stats?.total_datasets || 0}</h3>
              <p>مجموعة بيانات</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="profile-tabs">
        <button 
          className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          <span className="tab-icon">👤</span>
          المعلومات الشخصية
        </button>
        <button 
          className={`tab-btn ${activeTab === 'security' ? 'active' : ''}`}
          onClick={() => setActiveTab('security')}
        >
          <span className="tab-icon">🔒</span>
          الأمان والخصوصية
        </button>
        <button 
          className={`tab-btn ${activeTab === 'activity' ? 'active' : ''}`}
          onClick={() => setActiveTab('activity')}
        >
          <span className="tab-icon">📈</span>
          النشاط الأخير
        </button>
      </div>

      {/* Tab Content */}
      <div className="profile-content">
        {activeTab === 'profile' && (
          <div className="profile-section">
            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">📝</span>
                المعلومات الأساسية
              </h2>
              
              <div className="form-grid">
                <div className="form-field">
                  <label htmlFor="full_name">الاسم الكامل</label>
                  <input
                    type="text"
                    id="full_name"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    className={!isEditing ? 'disabled' : ''}
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="email">البريد الإلكتروني</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    className={!isEditing ? 'disabled' : ''}
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="phone">رقم الهاتف</label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    placeholder="+966 50 123 4567"
                    className={!isEditing ? 'disabled' : ''}
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="company">الشركة</label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    placeholder="اسم الشركة"
                    className={!isEditing ? 'disabled' : ''}
                  />
                </div>

                <div className="form-field full-width">
                  <label htmlFor="job_title">المسمى الوظيفي</label>
                  <input
                    type="text"
                    id="job_title"
                    name="job_title"
                    value={formData.job_title}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    placeholder="المسمى الوظيفي"
                    className={!isEditing ? 'disabled' : ''}
                  />
                </div>
              </div>

              {isEditing && (
                <div className="form-actions">
                  <button 
                    className="btn-save"
                    onClick={handleSave}
                    disabled={saving}
                  >
                    {saving ? 'جاري الحفظ...' : '💾 حفظ التغييرات'}
                  </button>
                  <button 
                    className="btn-cancel"
                    onClick={handleCancel}
                    disabled={saving}
                  >
                    ❌ إلغاء
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'security' && (
          <div className="profile-section">
            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">🔐</span>
                كلمة المرور
              </h2>
              
              <div className="security-info">
                <p className="info-text">
                  آخر تغيير لكلمة المرور كان منذ 30 يوماً
                </p>
                <button className="btn-change-password">
                  🔑 تغيير كلمة المرور
                </button>
              </div>
            </div>

            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">📱</span>
                المصادقة الثنائية
              </h2>
              
              <div className="security-option">
                <div className="option-info">
                  <h3>تفعيل المصادقة الثنائية</h3>
                  <p>احمِ حسابك بطبقة أمان إضافية</p>
                </div>
                <label className="toggle-switch">
                  <input type="checkbox" />
                  <span className="toggle-slider"></span>
                </label>
              </div>
            </div>

            <div className="section-card danger-zone">
              <h2 className="section-title">
                <span className="title-icon">⚠️</span>
                منطقة الخطر
              </h2>
              
              <div className="danger-actions">
                <button className="btn-danger">
                  🗑️ حذف الحساب نهائياً
                </button>
                <p className="danger-warning">
                  هذا الإجراء لا يمكن التراجع عنه. سيتم حذف جميع بياناتك نهائياً.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'activity' && (
          <div className="profile-section">
            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">📊</span>
                النشاط الأخير
              </h2>
              
              <div className="activity-timeline">
                <div className="activity-item">
                  <div className="activity-icon success">✓</div>
                  <div className="activity-content">
                    <h3>تم رفع 5 بطاقات جديدة</h3>
                    <p className="activity-time">منذ ساعتين</p>
                  </div>
                </div>

                <div className="activity-item">
                  <div className="activity-icon info">📝</div>
                  <div className="activity-content">
                    <h3>تم تحديث معلومات الملف الشخصي</h3>
                    <p className="activity-time">منذ 3 ساعات</p>
                  </div>
                </div>

                <div className="activity-item">
                  <div className="activity-icon success">✓</div>
                  <div className="activity-content">
                    <h3>تم تصدير مجموعة بيانات جديدة</h3>
                    <p className="activity-time">منذ يوم واحد</p>
                  </div>
                </div>

                <div className="activity-item">
                  <div className="activity-icon warning">⚡</div>
                  <div className="activity-content">
                    <h3>تم بدء معالجة دفعة جديدة</h3>
                    <p className="activity-time">منذ يومين</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;
