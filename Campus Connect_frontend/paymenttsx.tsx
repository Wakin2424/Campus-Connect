import React, { useState } from 'react';
import { ShoppingCart, User, Phone, Mail, MapPin, CreditCard } from 'lucide-react';

export default function PaymentPage() {
  const [selectedPayment, setSelectedPayment] = useState('paypal');
  const [mpesaPhone, setMpesaPhone] = useState('');
  const [formData, setFormData] = useState({
    fullName: '',
    phone: '',
    address1: '',
    address2: '',
    city: '',
    postalCode: '',
    country: 'Kenya'
  });

  const product = {
    name: 'Data Structures & Algorithms - Complete Guide',
    description: 'Comprehensive textbook with examples and practice problems',
    price: 2500,
    discount: 500,
    image: 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=500&fit=crop'
  };

  const seller = {
    name: 'John Kamau',
    phone: '+254 712 345 678',
    email: 'john.kamau@campusconnect.com'
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handlePayment = (method) => {
    if (method === 'paypal') {
      alert('Redirecting to PayPal checkout...');
    } else if (method === 'mpesa') {
      if (!mpesaPhone) {
        alert('Please enter your M-Pesa phone number');
        return;
      }
      alert(`STK push sent to ${mpesaPhone}. Please check your phone to complete payment.`);
    }
  };

  const totalPrice = product.price - product.discount;

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <div className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-[#0D1B2A] rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">CC</span>
                </div>
                <span className="text-xl font-bold text-[#0D1B2A]">Campus Connect</span>
              </div>
              <nav className="hidden md:flex space-x-6">
                <a href="#" className="text-[#0D1B2A] hover:text-[#1E90FF] font-medium transition">Home</a>
                <a href="#" className="text-[#0D1B2A] hover:text-[#1E90FF] font-medium transition">Market</a>
                <a href="#" className="text-[#0D1B2A] hover:text-[#1E90FF] font-medium transition">Notes</a>
                <a href="#" className="text-[#0D1B2A] hover:text-[#1E90FF] font-medium transition">Questions</a>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <ShoppingCart className="w-6 h-6 text-[#0D1B2A] cursor-pointer hover:text-[#1E90FF] transition" />
              <div className="w-10 h-10 bg-[#0D1B2A] rounded-full flex items-center justify-center cursor-pointer hover:bg-[#1E90FF] transition">
                <User className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold text-[#0D1B2A] mb-8">Complete Your Purchase</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Product, Address, Payment */}
          <div className="lg:col-span-2 space-y-8">
            {/* Product Details */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
              <h2 className="text-2xl font-bold text-[#0D1B2A] mb-6">Product Details</h2>
              <div className="flex flex-col sm:flex-row gap-6">
                <img 
                  src={product.image} 
                  alt={product.name}
                  className="w-full sm:w-48 h-64 object-cover rounded-xl"
                />
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-[#0D1B2A] mb-2">{product.name}</h3>
                  <p className="text-gray-600 mb-4">{product.description}</p>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500 line-through">KSh {product.price.toLocaleString()}</span>
                      <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">
                        Save KSh {product.discount.toLocaleString()}
                      </span>
                    </div>
                    <div className="text-3xl font-bold text-[#0D1B2A]">
                      KSh {totalPrice.toLocaleString()}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Address Details */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
              <h2 className="text-2xl font-bold text-[#0D1B2A] mb-6">Shipping / Delivery Address</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-[#0D1B2A] mb-2">Full Name</label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                    placeholder="Enter your full name"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-[#0D1B2A] mb-2">Phone Number</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                    placeholder="+254 700 000 000"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-[#0D1B2A] mb-2">Address Line 1</label>
                  <input
                    type="text"
                    name="address1"
                    value={formData.address1}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                    placeholder="Street address, P.O. Box"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-[#0D1B2A] mb-2">Address Line 2 (Optional)</label>
                  <input
                    type="text"
                    name="address2"
                    value={formData.address2}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                    placeholder="Apartment, suite, building, floor, etc."
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-[#0D1B2A] mb-2">City / Town</label>
                  <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                    placeholder="Enter city"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-[#0D1B2A] mb-2">Postal Code</label>
                  <input
                    type="text"
                    name="postalCode"
                    value={formData.postalCode}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                    placeholder="00100"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-[#0D1B2A] mb-2">Country</label>
                  <select
                    name="country"
                    value={formData.country}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                  >
                    <option>Kenya</option>
                    <option>Uganda</option>
                    <option>Tanzania</option>
                    <option>Rwanda</option>
                  </select>
                </div>
              </form>
            </div>

            {/* Payment Options */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
              <h2 className="text-2xl font-bold text-[#0D1B2A] mb-6">Choose Payment Method</h2>
              
              <div className="space-y-4">
                {/* PayPal */}
                <div 
                  onClick={() => setSelectedPayment('paypal')}
                  className={`p-6 rounded-xl border-2 cursor-pointer transition ${
                    selectedPayment === 'paypal' 
                      ? 'border-[#1E90FF] bg-blue-50' 
                      : 'border-gray-200 hover:border-[#1E90FF]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-[#0070BA] rounded-lg flex items-center justify-center">
                        <CreditCard className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h3 className="font-bold text-[#0D1B2A]">Pay with PayPal</h3>
                        <p className="text-sm text-gray-600">Fast and secure payment</p>
                      </div>
                    </div>
                    <div className={`w-6 h-6 rounded-full border-2 ${
                      selectedPayment === 'paypal' 
                        ? 'border-[#1E90FF] bg-[#1E90FF]' 
                        : 'border-gray-300'
                    }`}>
                      {selectedPayment === 'paypal' && (
                        <div className="w-full h-full flex items-center justify-center">
                          <div className="w-3 h-3 bg-white rounded-full"></div>
                        </div>
                      )}
                    </div>
                  </div>
                  {selectedPayment === 'paypal' && (
                    <button
                      onClick={() => handlePayment('paypal')}
                      className="w-full bg-[#0070BA] text-white py-3 rounded-lg font-semibold hover:bg-[#005EA6] transition"
                    >
                      Continue to PayPal
                    </button>
                  )}
                </div>

                {/* M-Pesa */}
                <div 
                  onClick={() => setSelectedPayment('mpesa')}
                  className={`p-6 rounded-xl border-2 cursor-pointer transition ${
                    selectedPayment === 'mpesa' 
                      ? 'border-[#1E90FF] bg-blue-50' 
                      : 'border-gray-200 hover:border-[#1E90FF]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center">
                        <Phone className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h3 className="font-bold text-[#0D1B2A]">Pay with M-Pesa</h3>
                        <p className="text-sm text-gray-600">Mobile money payment</p>
                      </div>
                    </div>
                    <div className={`w-6 h-6 rounded-full border-2 ${
                      selectedPayment === 'mpesa' 
                        ? 'border-[#1E90FF] bg-[#1E90FF]' 
                        : 'border-gray-300'
                    }`}>
                      {selectedPayment === 'mpesa' && (
                        <div className="w-full h-full flex items-center justify-center">
                          <div className="w-3 h-3 bg-white rounded-full"></div>
                        </div>
                      )}
                    </div>
                  </div>
                  {selectedPayment === 'mpesa' && (
                    <div className="space-y-3">
                      <p className="text-sm text-gray-600">You will receive an STK push on your phone.</p>
                      <input
                        type="tel"
                        value={mpesaPhone}
                        onChange={(e) => setMpesaPhone(e.target.value)}
                        placeholder="254 700 000 000"
                        className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#1E90FF] focus:ring-2 focus:ring-[#1E90FF] focus:ring-opacity-20 outline-none transition"
                      />
                      <button
                        onClick={() => handlePayment('mpesa')}
                        className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition"
                      >
                        Pay via M-Pesa
                      </button>
                    </div>
                  )}
                </div>

                {/* Contact Seller */}
                <div 
                  onClick={() => setSelectedPayment('contact')}
                  className={`p-6 rounded-xl border-2 cursor-pointer transition ${
                    selectedPayment === 'contact' 
                      ? 'border-[#1E90FF] bg-blue-50' 
                      : 'border-gray-200 hover:border-[#1E90FF]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-[#0D1B2A] rounded-full flex items-center justify-center">
                        <User className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h3 className="font-bold text-[#0D1B2A]">Contact Seller</h3>
                        <p className="text-sm text-gray-600">Arrange payment directly</p>
                      </div>
                    </div>
                    <div className={`w-6 h-6 rounded-full border-2 ${
                      selectedPayment === 'contact' 
                        ? 'border-[#1E90FF] bg-[#1E90FF]' 
                        : 'border-gray-300'
                    }`}>
                      {selectedPayment === 'contact' && (
                        <div className="w-full h-full flex items-center justify-center">
                          <div className="w-3 h-3 bg-white rounded-full"></div>
                        </div>
                      )}
                    </div>
                  </div>
                  {selectedPayment === 'contact' && (
                    <div className="bg-white rounded-lg p-4 space-y-3 border border-gray-200">
                      <p className="text-sm text-gray-600 mb-4">
                        Get in touch with the seller for manual payment or to negotiate the price.
                      </p>
                      <div className="flex items-center space-x-3">
                        <User className="w-5 h-5 text-[#0D1B2A]" />
                        <span className="font-semibold text-[#0D1B2A]">{seller.name}</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Phone className="w-5 h-5 text-[#0D1B2A]" />
                        <span className="text-gray-700">{seller.phone}</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Mail className="w-5 h-5 text-[#0D1B2A]" />
                        <span className="text-gray-700">{seller.email}</span>
                      </div>
                      <button className="w-full bg-[#0D1B2A] text-white py-3 rounded-lg font-semibold hover:bg-[#1E90FF] transition mt-4">
                        Contact Seller
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 sticky top-8">
              <h2 className="text-2xl font-bold text-[#0D1B2A] mb-6">Order Summary</h2>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-700">
                  <span>Product Price</span>
                  <span>KSh {product.price.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-green-600 font-semibold">
                  <span>Discount</span>
                  <span>- KSh {product.discount.toLocaleString()}</span>
                </div>
                <div className="border-t pt-4">
                  <div className="flex justify-between items-center">
                    <span className="text-lg font-bold text-[#0D1B2A]">Total Payable</span>
                    <span className="text-3xl font-bold text-[#0D1B2A]">
                      KSh {totalPrice.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              <div className="space-y-3 text-sm text-gray-600 bg-blue-50 p-4 rounded-lg">
                <div className="flex items-start space-x-2">
                  <MapPin className="w-4 h-4 mt-0.5 text-[#1E90FF]" />
                  <span>Free delivery within campus</span>
                </div>
                <div className="flex items-start space-x-2">
                  <CreditCard className="w-4 h-4 mt-0.5 text-[#1E90FF]" />
                  <span>Secure payment processing</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-[#0D1B2A] text-white mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-lg font-semibold mb-2">Campus Connect</p>
            <p className="text-gray-400 text-sm">Connecting students, sharing knowledge</p>
            <p className="text-gray-500 text-sm mt-4">© 2024 Campus Connect. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}