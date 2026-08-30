"""Bayesian linear regression with Gibbs sampling and a posterior predictive
check.

PyMC 5 is the production interface for this model (import pymc as pm) and is
listed in requirements.txt. This listing uses a conjugate normal-inverse-gamma
Gibbs sampler so the example runs without compiling PyTensor.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

SEED = 9
TRUE_ALPHA = 40.0
TRUE_BETA = 1.60


def rhat(chains):
    m, n = chains.shape
    chain_means = chains.mean(axis=1)
    grand = chain_means.mean()
    between = n * np.sum((chain_means - grand) ** 2) / (m - 1)
    within = chains.var(axis=1, ddof=1).mean()
    var_hat = ((n - 1) / n) * within + between / n
    return float(np.sqrt(var_hat / within))


def ess(draws):
    x = np.asarray(draws) - np.mean(draws)
    if x.size < 4 or np.allclose(x.var(), 0.0):
        return float(x.size)
    rho1 = float(np.corrcoef(x[:-1], x[1:])[0, 1])
    rho1 = min(max(rho1, -0.99), 0.99)
    tau = (1.0 + rho1) / (1.0 - rho1)
    return float(x.size / tau)


def gibbs(x, y, rng, n_draw=4000, n_burn=1000):
    n = y.size
    alpha = 0.0
    beta = 0.0
    sigma2 = 1.0
    a0 = 2.0
    b0 = 2.0
    v0 = 0.01
    keep_alpha = []
    keep_beta = []
    keep_sigma = []
    for i in range(n_draw + n_burn):
        prec_alpha = v0 + n / sigma2
        mean_alpha = ((y - beta * x).sum() / sigma2) / prec_alpha
        alpha = rng.normal(mean_alpha, np.sqrt(1.0 / prec_alpha))
        prec_beta = v0 + np.sum(x**2) / sigma2
        mean_beta = (np.sum(x * (y - alpha)) / sigma2) / prec_beta
        beta = rng.normal(mean_beta, np.sqrt(1.0 / prec_beta))
        resid = y - alpha - beta * x
        sigma2 = stats.invgamma.rvs(
            a0 + n / 2.0, scale=b0 + np.sum(resid**2) / 2.0, random_state=rng
        )
        if i >= n_burn:
            keep_alpha.append(alpha)
            keep_beta.append(beta)
            keep_sigma.append(np.sqrt(sigma2))
    return (
        np.asarray(keep_alpha),
        np.asarray(keep_beta),
        np.asarray(keep_sigma),
    )


rng = np.random.default_rng(SEED)
n = 250
discount = rng.normal(8.0, 2.0, size=n)
revenue = TRUE_ALPHA + TRUE_BETA * discount + rng.normal(0.0, 4.0, size=n)

chain1 = gibbs(discount, revenue, np.random.default_rng(SEED + 1))
chain2 = gibbs(discount, revenue, np.random.default_rng(SEED + 2))
alpha = np.concatenate([chain1[0], chain2[0]])
beta = np.concatenate([chain1[1], chain2[1]])
sigma = np.concatenate([chain1[2], chain2[2]])

print("estimand=posterior of the revenue-per-dollar discount slope")
print(f"beta_mean={beta.mean():.3f}")
print(
    f"beta_95ci=({np.quantile(beta, 0.025):.3f}, "
    f"{np.quantile(beta, 0.975):.3f})"
)
print(f"alpha_mean={alpha.mean():.3f}")
print(f"sigma_mean={sigma.mean():.3f}")
print(f"rhat_beta={rhat(np.vstack([chain1[1], chain2[1]])):.3f}")
print(f"ess_beta={ess(beta):.1f}")
print(f"rhat_alpha={rhat(np.vstack([chain1[0], chain2[0]])):.3f}")
print(f"ess_alpha={ess(alpha):.1f}")

idx = rng.integers(0, beta.size, size=n)
y_rep = alpha[idx] + beta[idx] * discount + rng.normal(0.0, sigma[idx])
print(f"ppc_obs_mean={revenue.mean():.3f} ppc_rep_mean={y_rep.mean():.3f}")
print(f"ppc_obs_sd={revenue.std():.3f} ppc_rep_sd={y_rep.std():.3f}")

fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].hist(beta, bins=30, color="0.35", edgecolor="white")
axes[0].set_xlabel("beta")
axes[0].set_ylabel("Draws")
axes[0].set_title("Posterior of the discount slope")
axes[1].hist(
    revenue, bins=20, density=True, alpha=0.6, label="Observed", color="0.2"
)
axes[1].hist(
    y_rep,
    bins=20,
    density=True,
    alpha=0.45,
    label="Posterior predictive",
    color="0.6",
)
axes[1].set_xlabel("Revenue")
axes[1].set_title("Posterior predictive check")
axes[1].legend()
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch9_bayesian_posterior.png", dpi=300, bbox_inches="tight"
)
plt.close()
print("Saved img/ch9_bayesian_posterior.png")
