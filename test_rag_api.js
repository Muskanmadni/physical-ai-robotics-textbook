/**
 * Simple test script to verify RAG backend API connection
 * Usage: node test_rag_api.js <backend_url>
 */

const { URL } = require('url');

async function testRAGAPI(backendUrl) {
  if (!backendUrl) {
    console.error('Error: Please provide the RAG backend URL as an argument');
    console.log('Usage: node test_rag_api.js <backend_url>');
    process.exit(1);
  }

  try {
    // Validate URL format
    new URL(backendUrl);
    
    console.log(`Testing RAG backend API at: ${backendUrl}`);
    
    // Test health endpoint
    console.log('\n1. Testing health endpoint...');
    const healthResponse = await fetch(`${backendUrl}/api/health`);
    const healthData = await healthResponse.json();
    
    if (healthResponse.ok) {
      console.log('✅ Health check successful:', healthData);
    } else {
      console.log('❌ Health check failed:', healthData);
    }

    // Test RAG query endpoint
    console.log('\n2. Testing RAG query endpoint...');
    const queryResponse = await fetch(`${backendUrl}/api/rag/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: 'What is Physical AI?',
      }),
    });
    
    const queryData = await queryResponse.json();
    
    if (queryResponse.ok) {
      console.log('✅ Query successful:', queryData);
    } else {
      console.log('❌ Query failed:', queryData);
    }

    console.log('\n3. Summary:');
    console.log(`Health endpoint: ${healthResponse.ok ? '✅' : '❌'}`);
    console.log(`Query endpoint: ${queryResponse.ok ? '✅' : '❌'}`);
    
    if (healthResponse.ok && queryResponse.ok) {
      console.log('\n🎉 Both endpoints are working correctly!');
      return true;
    } else {
      console.log('\n❌ There are issues with the API endpoints that need to be fixed.');
      return false;
    }
  } catch (error) {
    console.error('❌ Error testing API:', error.message);
    return false;
  }
}

// Run the test if this file is executed directly
if (require.main === module) {
  const backendUrl = process.argv[2];
  testRAGAPI(backendUrl);
}

module.exports = { testRAGAPI };