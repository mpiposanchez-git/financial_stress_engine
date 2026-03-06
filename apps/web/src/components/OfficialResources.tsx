export function OfficialResources() {
  return (
    <section className="result-card" aria-labelledby="official-resources-heading">
      <h2 id="official-resources-heading">Official resources</h2>
      <p className="resources-disclaimer">
        Information only: these links provide general guidance and are not personal financial advice.
      </p>
      <ul className="resources-list">
        <li>
          <a href="https://www.moneyhelper.org.uk/" target="_blank" rel="noreferrer">
            MoneyHelper
          </a>
        </li>
        <li>
          <a href="https://www.citizensadvice.org.uk/" target="_blank" rel="noreferrer">
            Citizens Advice
          </a>
        </li>
      </ul>
    </section>
  );
}
